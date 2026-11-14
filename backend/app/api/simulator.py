from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, Profile
from backend.app.models.simulator import Scenario
from backend.app.schemas.simulator import ForecastResponse, ScenarioCreate, ScenarioResponse
from backend.app.api.deps import get_current_user
from backend.app.agents.simulation_agent import simulation_agent
from backend.app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/simulator", tags=["Career Flight Simulator"])

@router.get("/forecast", response_model=ForecastResponse)
def get_forecast(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    forecast = simulation_agent.calculate_forecast(db, current_user.id)

    # Also compute 2 comparative baseline scenarios (e.g. at 6 hrs/wk and 12 hrs/wk)
    scenarios = []
    for test_hrs, name in [(6.0, "Light Pace (6 hrs/wk)"), (12.0, "Accelerated Pace (12 hrs/wk)")]:
        sc_res = simulation_agent.calculate_forecast(db, current_user.id, weekly_hours_override=test_hrs)
        scenarios.append(ScenarioResponse(
            name=name,
            target_career=sc_res["career_goal"],
            weekly_hours=test_hrs,
            pace_factor=sc_res["learner_pace_factor"],
            optimistic_date=sc_res["optimistic_date"],
            realistic_date=sc_res["realistic_date"],
            total_hours_needed=sc_res["total_gap_hours"],
            weeks_needed=sc_res["weeks_needed"],
            match_pct_4w=sc_res["match_pct_4w"],
            match_pct_8w=sc_res["match_pct_8w"],
            match_pct_12w=sc_res["match_pct_12w"],
            projection_points=sc_res["projection_points"],
            explanation=sc_res["explanation"]
        ))

    return ForecastResponse(
        career_goal=forecast["career_goal"],
        current_match_pct=forecast["current_match_pct"],
        total_gap_hours=forecast["total_gap_hours"],
        weekly_hours=forecast["weekly_hours"],
        learner_pace_factor=forecast["learner_pace_factor"],
        optimistic_date=forecast["optimistic_date"],
        realistic_date=forecast["realistic_date"],
        optimistic_weeks=forecast["optimistic_weeks"],
        realistic_weeks=forecast["realistic_weeks"],
        readiness_label=forecast["readiness_label"],
        explanation=forecast["explanation"],
        gaps_count=forecast["gaps_count"],
        comparison_scenarios=scenarios
    )

@router.post("/scenario", response_model=ScenarioResponse)
def run_what_if_scenario(
    scenario_req: ScenarioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sc_res = simulation_agent.calculate_forecast(
        db=db,
        user_id=current_user.id,
        career_slug_override=scenario_req.simulated_career,
        weekly_hours_override=scenario_req.weekly_hours,
        simulated_skill_levels=scenario_req.simulated_skills,
        simulate_fail=scenario_req.simulate_fail or False
    )

    return ScenarioResponse(
        name=scenario_req.name or "What-if Scenario",
        target_career=sc_res["career_goal"],
        weekly_hours=sc_res["weekly_hours"],
        pace_factor=sc_res["learner_pace_factor"],
        optimistic_date=sc_res["optimistic_date"],
        realistic_date=sc_res["realistic_date"],
        total_hours_needed=sc_res["total_gap_hours"],
        weeks_needed=sc_res["weeks_needed"],
        match_pct_4w=sc_res["match_pct_4w"],
        match_pct_8w=sc_res["match_pct_8w"],
        match_pct_12w=sc_res["match_pct_12w"],
        projection_points=sc_res["projection_points"],
        explanation=sc_res["explanation"]
    )

@router.post("/apply", response_model=ForecastResponse)
def apply_simulation_plan(
    scenario_req: ScenarioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    simulation_agent.save_and_apply_scenario(
        db=db,
        user_id=current_user.id,
        weekly_hours=scenario_req.weekly_hours,
        target_career_slug=scenario_req.simulated_career
    )

    # Rebuild roadmap with new schedule
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    slug = (scenario_req.simulated_career or profile.career_goal or "ai-ml-engineer").lower().replace(" ", "-").replace("/", "-")
    orchestrator.on_goal_changed(db, current_user.id, slug, reason=f"Applied Flight Simulator schedule of {scenario_req.weekly_hours} hrs/week")

    return get_forecast(current_user=current_user, db=db)

