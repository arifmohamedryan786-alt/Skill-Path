from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.roadmap import RoadmapStage, RoadmapItem, WeeklySprint
from backend.app.models.user import User, Profile
from backend.app.models.agent_log import AgentLog
from backend.app.schemas.roadmap import (
    RoadmapResponse, RoadmapStageOut, RoadmapItemOut,
    FirstWeekResponse, ItemStatusUpdate, SprintCompleteRequest
)
from backend.app.api.deps import get_current_user
from backend.app.agents.roadmap_planner_agent import roadmap_planner_agent
from backend.app.agents.learning_coach_agent import learning_coach_agent

router = APIRouter(tags=["Roadmap & Sprints"])

@router.get("/roadmap", response_model=RoadmapResponse)
def get_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    target_career = profile.career_goal if profile and profile.career_goal else "AI/ML Engineer"
    slug = target_career.lower().replace(" ", "-").replace("/", "-")

    stages = db.query(RoadmapStage).filter(RoadmapStage.user_id == current_user.id).order_by(RoadmapStage.stage_number).all()
    if not stages:
        # Build initial roadmap
        stages = roadmap_planner_agent.build_or_rebuild_roadmap(db, current_user.id, slug)

    stages_out = []
    total_items = 0
    completed_items = 0

    for stg in stages:
        items = db.query(RoadmapItem).filter(RoadmapItem.stage_id == stg.id).order_by(RoadmapItem.order).all()
        items_out = []
        for it in items:
            total_items += 1
            if it.status == "completed":
                completed_items += 1
            items_out.append(RoadmapItemOut(
                id=it.id,
                stage_id=it.stage_id,
                skill_id=it.skill_id,
                title=it.title,
                description=it.description,
                item_type=it.item_type,
                order=it.order,
                status=it.status,
                due_week=it.due_week,
                est_hours=it.est_hours,
                completed_at=it.completed_at
            ))

        stages_out.append(RoadmapStageOut(
            id=stg.id,
            stage_number=stg.stage_number,
            title=stg.title,
            description=stg.description,
            status=stg.status,
            est_weeks=stg.est_weeks,
            items=items_out
        ))

    progress_pct = round((completed_items / total_items * 100.0), 1) if total_items > 0 else 0.0

    return RoadmapResponse(
        career_goal=target_career,
        total_stages=len(stages_out),
        completed_stages=len([s for s in stages_out if s.status == "completed"]),
        overall_progress_pct=progress_pct,
        stages=stages_out,
        adjusted_for_year=profile.year if profile else 3,
        timeline_view={"total_weeks": 28, "view_mode": "12-month"}
    )

@router.post("/roadmap/regenerate", response_model=RoadmapResponse)
def regenerate_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    target_career = profile.career_goal if profile and profile.career_goal else "AI/ML Engineer"
    slug = target_career.lower().replace(" ", "-").replace("/", "-")

    roadmap_planner_agent.build_or_rebuild_roadmap(db, current_user.id, slug)

    # Log action
    log = AgentLog(
        user_id=current_user.id,
        agent_name="Roadmap Planner Agent",
        action="Manually Regenerated Roadmap",
        reason=f"Regenerated 7-stage roadmap aligned with {target_career}.",
        details={"career": target_career}
    )
    db.add(log)
    db.commit()

    return get_roadmap(current_user=current_user, db=db)

@router.get("/roadmap/first-week", response_model=FirstWeekResponse)
def get_first_week_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    weekly_hours = profile.weekly_hours if profile else 8.0
    return learning_coach_agent.generate_first_week_plan(db, current_user.id, weekly_hours=weekly_hours)

@router.put("/roadmap/{item_id}/status")
def update_item_status(
    item_id: int,
    status_update: ItemStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(RoadmapItem).filter(
        RoadmapItem.id == item_id,
        RoadmapItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap item not found")

    item.status = status_update.status
    if status_update.status == "completed":
        item.completed_at = datetime.utcnow()
    db.commit()
    return {"message": "Status updated successfully", "status": item.status}

@router.get("/sprint/current")
def get_current_sprint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sprint = db.query(WeeklySprint).filter(
        WeeklySprint.user_id == current_user.id,
        WeeklySprint.status == "active"
    ).first()

    if not sprint:
        # Create initial sprint from First Week plan
        first_week = learning_coach_agent.generate_first_week_plan(db, current_user.id)
        sprint = WeeklySprint(
            user_id=current_user.id,
            week_number=1,
            title="Sprint 1: Core Foundations",
            focus_summary=first_week["focus_topic"],
            target_hours=first_week["weekly_hours"],
            tasks=first_week["tasks"],
            status="active"
        )
        db.add(sprint)
        db.commit()
        db.refresh(sprint)

    return {
        "sprint_id": sprint.id,
        "week_number": sprint.week_number,
        "title": sprint.title,
        "focus_summary": sprint.focus_summary,
        "target_hours": sprint.target_hours,
        "tasks": sprint.tasks,
        "status": sprint.status
    }

@router.post("/sprint/complete")
def complete_sprint(
    req: SprintCompleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sprint = db.query(WeeklySprint).filter(
        WeeklySprint.id == req.sprint_id,
        WeeklySprint.user_id == current_user.id
    ).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    sprint.status = "completed"
    sprint.completed_at = datetime.utcnow()

    # Create next sprint
    next_sprint = WeeklySprint(
        user_id=current_user.id,
        week_number=sprint.week_number + 1,
        title=f"Sprint {sprint.week_number + 1}: Data & Framework Application",
        focus_summary="Deepening practical hands-on exercises",
        target_hours=sprint.target_hours,
        tasks=[
            {"day": "Monday", "duration_mins": 45, "title": "Data Structures & Lists", "completed": False},
            {"day": "Wednesday", "duration_mins": 60, "title": "Solving Algorithmic Puzzles", "completed": False},
            {"day": "Friday", "duration_mins": 60, "title": "Connecting to SQLite Database", "completed": False}
        ],
        status="active"
    )
    db.add(next_sprint)

    log = AgentLog(
        user_id=current_user.id,
        agent_name="Learning Coach Agent",
        action="Completed Sprint",
        reason=f"Learner completed Sprint {sprint.week_number}. Rolled over into Sprint {sprint.week_number + 1}.",
        details={"completed_sprint": sprint.week_number}
    )
    db.add(log)
    db.commit()

    return {"message": "Sprint marked completed", "next_week": sprint.week_number + 1}

