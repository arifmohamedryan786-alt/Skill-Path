from typing import Optional, Any
from pydantic import BaseModel

class VerifiedSkillOut(BaseModel):
    id: int
    skill_id: int
    skill_name: str
    category: str
    verified_level: int
    score_pct: float
    evidence_type: str
    evidence_ref: str
    verification_hash: str
    verified_at: str

class PassportSettingsUpdate(BaseModel):
    is_public: Optional[bool] = None
    show_scores: Optional[bool] = None
    show_evidence: Optional[bool] = None

class PassportOut(BaseModel):
    id: int
    slug: str
    full_name: str
    target_career: str
    readiness_pct: float
    is_public: bool
    show_scores: bool
    show_evidence: bool
    verified_skills: list[VerifiedSkillOut]
    all_skills: list[dict[str, Any]]
    public_url: str
    qr_data_url: Optional[str] = None

class PassportPublicOut(BaseModel):
    slug: str
    full_name: str
    education: str
    branch: str
    target_career: str
    readiness_pct: float
    verified_skills: list[VerifiedSkillOut]
    verified_count: int

class VerifyHashResponse(BaseModel):
    skill_name: str
    is_valid: bool
    stored_hash: str
    recomputed_hash: str
    timestamp: str
    details: str

