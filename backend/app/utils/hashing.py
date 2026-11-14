import hashlib

def compute_verification_hash(user_id: int, skill_slug: str, score_pct: float, date_str: str) -> str:
    """
    Computes a deterministic cryptographic SHA-256 fingerprint:
    hash(user_id:skill_slug:score_pct:date_str:SALT)
    """
    salt = "SkillPath-Verified-Badge-Crypto-Salt-v1"
    # Format score to 1 decimal place to ensure exact string stability
    normalized_score = f"{float(score_pct):.1f}"
    payload = f"{user_id}:{skill_slug}:{normalized_score}:{date_str}:{salt}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def verify_skill_hash(stored_hash: str, user_id: int, skill_slug: str, score_pct: float, date_str: str) -> bool:
    """
    Validates if the stored hash matches recomputed hash from primary records.
    """
    expected_hash = compute_verification_hash(user_id, skill_slug, score_pct, date_str)
    return stored_hash == expected_hash

