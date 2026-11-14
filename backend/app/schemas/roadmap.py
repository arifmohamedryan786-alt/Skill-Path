from typing import Optional, Any
from pydantic import BaseModel

class RoadmapItemOut(BaseModel):
    id: int
    stage_id: int
    skill_id: Optional[int]
    title: str
    description: str
    item_type: str
    order: int
    status: str
    due_week: int
    est_hours: float
    completed_at: Optional[Any] = None

class RoadmapStageOut(BaseModel):
    id: int
    stage_number: int
    title: str
    description: str
    status: str
    est_weeks: int
    items: list[RoadmapItemOut]

class RoadmapResponse(BaseModel):
    career_goal: str
    total_stages: int
    completed_stages: int
    overall_progress_pct: float
    stages: list[RoadmapStageOut]
    adjusted_for_year: int
    timeline_view: dict[str, Any]

class FirstWeekTask(BaseModel):
    day: str
    duration_mins: int
    title: str
    description: str
    action_url: Optional[str] = None
    completed: bool = False

class FirstWeekResponse(BaseModel):
    focus_topic: str
    why_it_matters: str
    weekly_hours: float
    tasks: list[FirstWeekTask]

class ItemStatusUpdate(BaseModel):
    status: str # "pending", "in_progress", "completed", "skipped"

class SprintCompleteRequest(BaseModel):
    sprint_id: int

