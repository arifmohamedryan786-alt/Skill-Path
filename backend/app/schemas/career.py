from typing import Optional, Any
from pydantic import BaseModel

class CareerSkillItem(BaseModel):
    skill_id: int
    name: str
    category: str
    target_level: int
    weight: int
    plain_explanation: str

class CareerOut(BaseModel):
    id: int
    slug: str
    name: str
    plain_description: str
    demand_level: str
    salary_range_note: str
    suits_who: str
    entry_titles: list[str]

    class Config:
        from_attributes = True

class CareerDetailOut(CareerOut):
    day_in_life: str
    typical_tasks: list[str]
    growth_path: list[str]
    mini_project: dict[str, Any]
    skills: list[CareerSkillItem]

class CareerCompareRequest(BaseModel):
    career_ids: list[int]

class CareerCompareResponse(BaseModel):
    careers: list[CareerDetailOut]
    common_skills: list[str]
    distinct_skills: dict[str, list[str]]

class CareerShortlistRequest(BaseModel):
    career_id: int
    is_primary: Optional[bool] = False
    notes: Optional[str] = ""

class CareerShortlistOut(BaseModel):
    id: int
    career_id: int
    name: str
    slug: str
    is_primary: bool
    notes: str
    created_at: Any

class TryItResponse(BaseModel):
    career_id: int
    career_name: str
    title: str
    duration: str
    summary: str
    steps: list[dict[str, Any]]
    starter_code: Optional[str] = None
    expected_outcome: str

