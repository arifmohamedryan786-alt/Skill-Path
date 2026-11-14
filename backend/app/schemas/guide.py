from typing import Optional, Any
from pydantic import BaseModel

class CareerGuideResponse(BaseModel):
    version: int
    target_career: str
    generated_at: str
    where_you_stand: str
    top_careers_summary: str
    skills_sequence: str
    recommended_courses: list[dict[str, Any]]
    projects_plan: dict[str, Any] # {"beginner": "...", "intermediate": "...", "capstone": "..."}
    internship_strategy: str
    growth_options: str # certifications, competitions, open source, higher studies (GATE/GRE)
    twelve_month_plan: list[dict[str, Any]]
    next_7_days: list[dict[str, Any]]

