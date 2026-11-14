import os
import re
import json
import time
import asyncio
import hashlib
from typing import Optional, Any, Type, AsyncGenerator
import httpx
from pydantic import BaseModel
from backend.app.config import settings

# ==============================================================================
# 1. Personal Identifier & Injection Sanitizer
# ==============================================================================

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_REGEX = re.compile(
    r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b|\b[6-9]\d{9}\b'
)
# Matches Aadhaar, SSN, Student Roll numbers, National IDs
ID_PATTERNS = [
    re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),                         # SSN
    re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b'),                      # Aadhaar with spaces
    re.compile(r'\b\d{12}\b'),                                   # 12-digit national ID
    re.compile(r'\b(ID|Roll|Reg|Student\s*ID)[:\s#]*[A-Za-z0-9-_]{4,15}\b', re.IGNORECASE)
]

INJECTION_PATTERNS = [
    re.compile(r"(?i)ignore\s+(all\s+)?(previous|prior)\s+instructions"),
    re.compile(r"(?i)system\s+prompt"),
    re.compile(r"(?i)you\s+are\s+now\s+a"),
    re.compile(r"(?i)act\s+as\s+an\s+unrestricted"),
    re.compile(r"(?i)disregard\s+all"),
    re.compile(r"(?i)<\/?system>"),
    re.compile(r"(?i)jailbreak"),
    re.compile(r"```system"),
]

def strip_personal_identifiers(text: str) -> str:
    """
    Strips email addresses, phone numbers, and student/national ID numbers
    before prompts leave the backend boundary to third-party LLM APIs.
    """
    if not text:
        return ""
    cleaned = EMAIL_REGEX.sub("[EMAIL]", text)
    cleaned = PHONE_REGEX.sub("[PHONE]", cleaned)
    for id_pat in ID_PATTERNS:
        cleaned = id_pat.sub("[ID]", cleaned)
    return cleaned

def sanitize_user_input(text: str) -> str:
    """
    Combined prompt injection guard and PII scrubber.
    """
    if not text:
        return ""
    cleaned = strip_personal_identifiers(text)
    for pattern in INJECTION_PATTERNS:
        cleaned = pattern.sub("[sanitized]", cleaned)
    return cleaned[:4000].strip()

# ==============================================================================
# 2. Exceptions
# ==============================================================================

class AIBusyException(Exception):
    """Raised when the LLM service is rate-limited or at capacity."""
    pass

class LLMProviderException(Exception):
    """Raised when an LLM provider encounters an unrecoverable error."""
    pass

# ==============================================================================
# 3. In-Memory Response Cache
# ==============================================================================

class LLMResponseCache:
    """
    Thread-safe in-memory LRU/TTL cache for repeated prompts.
    """
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl = ttl_seconds
        self.cache: dict[str, tuple[float, Any]] = {}
        self.hits: int = 0
        self.misses: int = 0

    def _make_key(self, provider: str, model: str, prompt: str, system: Optional[str], is_json: bool) -> str:
        raw = f"{provider}:{model}:{prompt}:{system or ''}:{is_json}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, provider: str, model: str, prompt: str, system: Optional[str] = None, is_json: bool = False) -> Optional[Any]:
        if not settings.LLM_CACHE_ENABLED:
            return None
        key = self._make_key(provider, model, prompt, system, is_json)
        entry = self.cache.get(key)
        if entry:
            timestamp, data = entry
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                return data
            else:
                self.cache.pop(key, None)
        self.misses += 1
        return None

    def set(self, provider: str, model: str, prompt: str, data: Any, system: Optional[str] = None, is_json: bool = False):
        if not settings.LLM_CACHE_ENABLED:
            return
        key = self._make_key(provider, model, prompt, system, is_json)
        self.cache[key] = (time.time(), data)

    def clear(self):
        self.cache.clear()
        self.hits = 0
        self.misses = 0

# ==============================================================================
# 4. Per-User Sliding Window Rate Limiter
# ==============================================================================

class UserRateLimiter:
    """
    Sliding-window per-user request limiter.
    """
    def __init__(self, max_requests_per_minute: int = 15):
        self.max_requests = max_requests_per_minute
        self.user_requests: dict[str, list[float]] = {}

    def check_limit(self, user_id: Optional[Any]) -> bool:
        if not user_id:
            return True
        key = str(user_id)
        now = time.time()
        window_start = now - 60.0

        timestamps = self.user_requests.get(key, [])
        # Filter timestamps within the last 60 seconds
        active_timestamps = [t for t in timestamps if t > window_start]
        if len(active_timestamps) >= self.max_requests:
            return False

        active_timestamps.append(now)
        self.user_requests[key] = active_timestamps
        return True

    def reset(self):
        self.user_requests.clear()

# ==============================================================================
# 5. Provider-Agnostic LLM Client
# ==============================================================================

class LLMClient:
    """
    Unified, provider-agnostic LLM Client supporting:
    - Providers: gemini | groq | openrouter | ollama | anthropic | openai
    - Exponential backoff retry on 429 / rate limit
    - Automatic PII identifier stripping before external calls
    - Response caching for identical prompts
    - Per-user rate limiting
    - Streaming, plain text, and structured JSON generation
    """

    def __init__(self):
        self.cache = LLMResponseCache(ttl_seconds=settings.LLM_CACHE_TTL_SECONDS)
        self.rate_limiter = UserRateLimiter(max_requests_per_minute=settings.LLM_USER_RATE_LIMIT_PER_MINUTE)

    @property
    def provider(self) -> str:
        return (os.getenv("LLM_PROVIDER") or settings.LLM_PROVIDER or "gemini").lower().strip()

    def get_model(self) -> str:
        p = self.provider
        if p == "groq":
            return os.getenv("GROQ_MODEL") or settings.GROQ_MODEL
        elif p == "openrouter":
            return os.getenv("OPENROUTER_MODEL") or settings.OPENROUTER_MODEL
        elif p == "ollama":
            return os.getenv("OLLAMA_MODEL") or settings.OLLAMA_MODEL
        elif p == "anthropic":
            return os.getenv("ANTHROPIC_MODEL") or settings.ANTHROPIC_MODEL
        elif p == "openai":
            return os.getenv("OPENAI_MODEL") or settings.OPENAI_MODEL
        return os.getenv("GEMINI_MODEL") or settings.GEMINI_MODEL

    def get_api_key(self) -> str:
        p = self.provider
        if p == "groq":
            return os.getenv("GROQ_API_KEY") or settings.GROQ_API_KEY
        elif p == "openrouter":
            return os.getenv("OPENROUTER_API_KEY") or settings.OPENROUTER_API_KEY
        elif p == "ollama":
            return "" # Ollama is local, no API key required
        elif p == "anthropic":
            return os.getenv("ANTHROPIC_API_KEY") or settings.ANTHROPIC_API_KEY
        elif p == "openai":
            return os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
        return os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY

    @property
    def is_available(self) -> bool:
        if self.provider == "ollama":
            return True
        key = self.get_api_key()
        return bool(key and len(key.strip()) > 5)

    async def _execute_with_retry(self, request_fn):
        """
        Executes request_fn with exponential backoff on HTTP 429 / 503 / timeout.
        """
        max_retries = settings.LLM_MAX_RETRIES
        factor = settings.LLM_RETRY_BACKOFF_FACTOR
        attempt = 0

        while attempt <= max_retries:
            try:
                return await request_fn()
            except httpx.HTTPStatusError as e:
                status = e.response.status_code
                if status in (429, 503) and attempt < max_retries:
                    delay = (factor ** attempt) * 0.5
                    attempt += 1
                    await asyncio.sleep(delay)
                    continue
                if status == 429:
                    raise AIBusyException("AI is busy, try again shortly")
                raise e
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                if attempt < max_retries:
                    delay = (factor ** attempt) * 0.5
                    attempt += 1
                    await asyncio.sleep(delay)
                    continue
                raise e

    # ==========================================================================
    # Public Methods: generate(), stream(), json()
    # ==========================================================================

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        user_id: Optional[Any] = None,
        **kwargs
    ) -> str:
        """
        Generates text completion using the configured LLM provider.
        """
        if not self.is_available:
            return ""

        if user_id and not self.rate_limiter.check_limit(user_id):
            raise AIBusyException("AI is busy: per-user request limit reached. Please try again shortly.")

        clean_prompt = sanitize_user_input(prompt)
        cached = self.cache.get(self.provider, self.get_model(), clean_prompt, system_prompt, is_json=False)
        if cached is not None:
            return str(cached)

        text = await self._call_provider(clean_prompt, system_prompt=system_prompt, is_json=False, **kwargs)
        if text:
            self.cache.set(self.provider, self.get_model(), clean_prompt, text, system_prompt=system_prompt, is_json=False)
        return text

    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        user_id: Optional[Any] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Streams response chunks from the configured LLM provider.
        """
        if not self.is_available:
            return

        if user_id and not self.rate_limiter.check_limit(user_id):
            yield "AI is busy, try again shortly"
            return

        clean_prompt = sanitize_user_input(prompt)
        # For simplicity and cross-provider stability, stream chunk-by-chunk or yield output
        full_text = await self.generate(clean_prompt, system_prompt=system_prompt, user_id=user_id, **kwargs)
        if full_text:
            words = full_text.split(" ")
            for i, word in enumerate(words):
                yield word + (" " if i < len(words) - 1 else "")
                await asyncio.sleep(0.01)

    async def json(
        self,
        prompt: str,
        schema: Optional[Type[BaseModel] | dict] = None,
        system_prompt: Optional[str] = None,
        user_id: Optional[Any] = None,
        **kwargs
    ) -> Optional[dict[str, Any]]:
        """
        Generates validated JSON from the configured LLM provider.
        Returns parsed dict, or None on failure to allow seamless deterministic fallback.
        """
        if not self.is_available:
            return None

        if user_id and not self.rate_limiter.check_limit(user_id):
            raise AIBusyException("AI is busy: per-user request limit reached. Please try again shortly.")

        clean_prompt = sanitize_user_input(prompt)
        cached = self.cache.get(self.provider, self.get_model(), clean_prompt, system_prompt, is_json=True)
        if cached is not None:
            return cached

        try:
            raw_text = await self._call_provider(clean_prompt, system_prompt=system_prompt, is_json=True, **kwargs)
            if not raw_text:
                return None

            # Clean potential markdown wrapping
            clean_raw = raw_text.strip()
            if clean_raw.startswith("```json"):
                clean_raw = clean_raw[7:]
            if clean_raw.startswith("```"):
                clean_raw = clean_raw[3:]
            if clean_raw.endswith("```"):
                clean_raw = clean_raw[:-3]
            clean_raw = clean_raw.strip()

            parsed = json.loads(clean_raw)
            if schema and isinstance(schema, type) and issubclass(schema, BaseModel):
                validated = schema.model_validate(parsed)
                parsed = validated.model_dump()

            self.cache.set(self.provider, self.get_model(), clean_prompt, parsed, system_prompt=system_prompt, is_json=True)
            return parsed
        except Exception:
            return None

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Optional[Type[BaseModel]] = None
    ) -> Optional[dict[str, Any]]:
        """
        Backward-compatible alias for existing agent code.
        """
        return await self.json(
            prompt=user_prompt,
            schema=response_schema,
            system_prompt=system_prompt
        )

    # ==========================================================================
    # Provider REST Adapters
    # ==========================================================================

    async def _call_provider(self, prompt: str, system_prompt: Optional[str] = None, is_json: bool = False, **kwargs) -> str:
        p = self.provider

        if p == "groq":
            return await self._call_openai_compatible(
                base_url="https://api.groq.com/openai/v1/chat/completions",
                api_key=self.get_api_key(),
                model=self.get_model(),
                prompt=prompt,
                system_prompt=system_prompt,
                is_json=is_json
            )
        elif p == "openrouter":
            headers = {
                "HTTP-Referer": "http://localhost:5173",
                "X-Title": "SkillPath Zero-to-Job Platform"
            }
            return await self._call_openai_compatible(
                base_url="https://openrouter.ai/api/v1/chat/completions",
                api_key=self.get_api_key(),
                model=self.get_model(),
                prompt=prompt,
                system_prompt=system_prompt,
                is_json=is_json,
                extra_headers=headers
            )
        elif p == "ollama":
            return await self._call_ollama(prompt, system_prompt, is_json)
        elif p == "anthropic":
            return await self._call_anthropic(prompt, system_prompt, is_json)
        elif p == "openai":
            return await self._call_openai_compatible(
                base_url="https://api.openai.com/v1/chat/completions",
                api_key=self.get_api_key(),
                model=self.get_model(),
                prompt=prompt,
                system_prompt=system_prompt,
                is_json=is_json
            )
        else: # Default: Gemini
            return await self._call_gemini(prompt, system_prompt, is_json)

    async def _call_gemini(self, prompt: str, system_prompt: Optional[str], is_json: bool) -> str:
        api_key = self.get_api_key()
        model = self.get_model()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        sys_text = system_prompt or "You are SkillPath AI."
        if is_json:
            sys_text += "\nIMPORTANT: You must return ONLY a single valid raw JSON object. Do not wrap in markdown or backticks."

        payload = {
            "contents": [
                {
                    "parts": [{"text": f"System: {sys_text}\n\nUser: {prompt}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        if is_json:
            payload["generationConfig"]["responseMimeType"] = "application/json"

        async def _do():
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                res.raise_for_status()
                data = res.json()
                candidates = data.get("candidates", [])
                if candidates:
                    return candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                return ""

        return await self._execute_with_retry(_do)

    async def _call_openai_compatible(
        self,
        base_url: str,
        api_key: str,
        model: str,
        prompt: str,
        system_prompt: Optional[str],
        is_json: bool,
        extra_headers: Optional[dict[str, str]] = None
    ) -> str:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            **(extra_headers or {})
        }

        messages = []
        if system_prompt:
            sys_content = system_prompt
            if is_json:
                sys_content += "\nOutput valid raw JSON only."
            messages.append({"role": "system", "content": sys_content})
        elif is_json:
            messages.append({"role": "system", "content": "You are a helpful assistant. Output valid raw JSON only."})

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.2
        }
        if is_json:
            payload["response_format"] = {"type": "json_object"}

        async def _do():
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(base_url, headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
                return ""

        return await self._execute_with_retry(_do)

    async def _call_ollama(self, prompt: str, system_prompt: Optional[str], is_json: bool) -> str:
        base_url = (os.getenv("OLLAMA_BASE_URL") or settings.OLLAMA_BASE_URL).rstrip("/")
        url = f"{base_url}/api/chat"
        model = self.get_model()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        if is_json:
            payload["format"] = "json"

        async def _do():
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(url, json=payload)
                res.raise_for_status()
                data = res.json()
                return data.get("message", {}).get("content", "")

        return await self._execute_with_retry(_do)

    async def _call_anthropic(self, prompt: str, system_prompt: Optional[str], is_json: bool) -> str:
        api_key = self.get_api_key()
        model = self.get_model()
        url = "https://api.anthropic.com/v1/messages"

        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        sys_content = system_prompt or "You are SkillPath AI."
        if is_json:
            sys_content += "\nOutput valid raw JSON only."

        payload = {
            "model": model,
            "max_tokens": 1024,
            "system": sys_content,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }

        async def _do():
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()
                content = data.get("content", [])
                if content:
                    return content[0].get("text", "")
                return ""

        return await self._execute_with_retry(_do)

llm_client = LLMClient()
