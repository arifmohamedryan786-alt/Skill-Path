from typing import Optional, Any
from pydantic import BaseModel

class DiscoveryQuestion(BaseModel):
    id: int
    category: str # "interests", "subjects", "work_style", "aptitude"
    question: str
    help_text: Optional[str] = None
    options: list[dict[str, Any]] # [{"value": "build_apps", "label": "Building interactive apps & tools", "traits": {"coding": 3, "engineering": 2}}]
    type: str = "single" # "single", "multiple", "puzzle"

class DiscoverySubmitRequest(BaseModel):
    answers: dict[str, Any] # {"q1": "build_apps", "q2": ["math", "cs"], ...}

class CareerMatchResult(BaseModel):
    career_id: int
    slug: str
    name: str
    match_pct: float
    plain_reason: str
    suits_who: str
    demand_level: str
    entry_titles: list[str]

class DiscoveryResultResponse(BaseModel):
    top_careers: list[CareerMatchResult]
    aptitude_scores: dict[str, float]
    summary_message: str

