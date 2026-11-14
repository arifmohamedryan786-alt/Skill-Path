from typing import Optional, Any
from pydantic import BaseModel

class ScenarioCreate(BaseModel):
    name: Optional[str] = "What-if Scenario"
    weekly_hours: float
    simulated_skills: dict[str, int] = {} # {skill_slug: simulated_level}
    simulated_career: Optional[str] = None
    simulate_fail: Optional[bool] = False

class ScenarioResponse(BaseModel):
    id: Optional[int] = None
    name: str
    target_career: str
    weekly_hours: float
    pace_factor: float
    optimistic_date: str
    realistic_date: str
    total_hours_needed: float
    weeks_needed: int
    match_pct_4w: float
    match_pct_8w: float
    match_pct_12w: float
    projection_points: list[dict[str, Any]] # [{"week": 0, "match": 15}, {"week": 4, "match": 40}, ...]
    explanation: str

class ForecastResponse(BaseModel):
    career_goal: str
    current_match_pct: float
    total_gap_hours: float
    weekly_hours: float
    learner_pace_factor: float
    optimistic_date: str
    realistic_date: str
    optimistic_weeks: int
    realistic_weeks: int
    readiness_label: str
    explanation: str
    gaps_count: int
    comparison_scenarios: list[ScenarioResponse] = []

