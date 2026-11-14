from typing import Optional, Any
from pydantic import BaseModel

class ProfileBase(BaseModel):
    full_name: str
    education: Optional[str] = "B.Tech"
    branch: Optional[str] = ""
    year: Optional[int] = 1
    institution: Optional[str] = ""
    interests: list[str] = []
    strengths: list[str] = []
    certifications: list[str] = []
    projects: list[dict[str, Any]] = []
    career_goal: Optional[str] = ""
    goal_status: Optional[str] = "unknown" # "known", "rough", "unknown"
    weekly_hours: Optional[float] = 8.0
    language: Optional[str] = "en"

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    education: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[int] = None
    institution: Optional[str] = None
    interests: Optional[list[str]] = None
    strengths: Optional[list[str]] = None
    certifications: Optional[list[str]] = None
    projects: Optional[list[dict[str, Any]]] = None
    career_goal: Optional[str] = None
    goal_status: Optional[str] = None
    weekly_hours: Optional[float] = None
    language: Optional[str] = None

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    learner_pace_factor: float
    cohort_id: Optional[int] = None

    class Config:
        from_attributes = True

class ResumeParseRequest(BaseModel):
    resume_text: str

class ResumeParseResponse(BaseModel):
    extracted_skills: list[str]
    extracted_projects: list[dict[str, Any]]
    extracted_education: Optional[str] = None
    extracted_branch: Optional[str] = None
    extracted_year: Optional[int] = None
    summary: str

