import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

def _get_cors_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "")
    if raw and raw.strip():
        origins = [o.strip() for o in raw.split(",") if o.strip() and o.strip() != "*"]
        if origins:
            return origins
    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="allow")

    PROJECT_NAME: str = "SkillPath"
    API_V1_STR: str = ""
    SECRET_KEY: str = os.getenv("SECRET_KEY", "skillpath-super-secure-production-ready-jwt-secret-key-2025")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/skillpath.db")
    
    # LLM Provider Configuration (gemini | groq | openrouter | ollama | anthropic | openai)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    
    # Gemini (Default Free Tier)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Groq (Fast Free Tier)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # OpenRouter
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
    
    # Ollama (Local)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # Anthropic
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # LLM Resilience & Safeguards
    LLM_MAX_RETRIES: int = 3
    LLM_RETRY_BACKOFF_FACTOR: float = 1.5
    LLM_USER_RATE_LIMIT_PER_MINUTE: int = 15
    LLM_CACHE_ENABLED: bool = True
    LLM_CACHE_TTL_SECONDS: int = 3600
    
    # CORS Origins (Comma-separated from env, '*' stripped for production security)
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000")
    BACKEND_CORS_ORIGINS: list[str] = _get_cors_origins()

settings = Settings()

