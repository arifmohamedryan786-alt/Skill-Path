from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, Profile
from backend.app.models.resource import Resource
from backend.app.models.glossary import Glossary
from backend.app.models.career import Career
from backend.app.models.roadmap import RoadmapItem, RoadmapStage
from backend.app.models.assessment import AssessmentResult
from backend.app.api.deps import get_current_user
from backend.app.agents.career_matcher_agent import career_matcher_agent
from backend.app.agents.skill_analyst_agent import skill_analyst_agent

router = APIRouter(tags=["General Analytics & Resources"])

@router.get("/resources")
def list_resources(
    skill_slug: str = "",
    type: str = "",
    db: Session = Depends(get_db)
):
    query = db.query(Resource)
    if type:
        query = query.filter(Resource.type == type)
    resources = query.limit(50).all()

    return [
        {
            "id": r.id,
            "title": r.title,
            "type": r.type,
            "url": r.url,
            "difficulty": r.difficulty,
            "duration": r.duration,
            "provider": r.provider,
            "free": r.free,
            "skill_id": r.skill_id
        }
        for r in resources
    ]

@router.get("/glossary")
def get_glossary(category: str = "", db: Session = Depends(get_db)):
    query = db.query(Glossary)
    if category:
        query = query.filter(Glossary.category == category)
    items = query.order_by(Glossary.term.asc()).all()

    return [
        {
            "id": g.id,
            "term": g.term,
            "category": g.category,
            "plain_meaning": g.plain_meaning,
            "example": g.example or ""
        }
        for g in items
    ]

@router.get("/match")
def get_career_match(
    career_id: int = 1,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if profile and profile.career_goal:
        c = db.query(Career).filter(Career.name.ilike(f"%{profile.career_goal}%")).first()
        if c:
            career_id = c.id
    return career_matcher_agent.calculate_match(db, current_user.id, career_id)

@router.get("/analysis")
def get_skill_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return skill_analyst_agent.analyze_user_skills(db, current_user.id)

@router.get("/progress")
def get_learning_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    items = db.query(RoadmapItem).filter(RoadmapItem.user_id == current_user.id).all()
    stages = db.query(RoadmapStage).filter(RoadmapStage.user_id == current_user.id).all()
    results = db.query(AssessmentResult).filter(AssessmentResult.user_id == current_user.id).order_by(AssessmentResult.created_at.asc()).all()

    total_tasks = len(items)
    completed_tasks = len([i for i in items if i.status == "completed"])
    overall_progress = round((completed_tasks / max(total_tasks, 1)) * 100.0, 1) if total_tasks > 0 else 0.0

    score_trend = [
        {"test": f"Test #{idx + 1}", "score": r.score_pct, "date": r.created_at.strftime("%d %b")}
        for idx, r in enumerate(results)
    ]

    return {
        "overall_progress_pct": overall_progress,
        "completed_items": completed_tasks,
        "total_items": total_tasks,
        "stages_unlocked": len([s for s in stages if s.status != "locked"]),
        "total_stages": len(stages) or 7,
        "pace_factor": profile.learner_pace_factor if profile else 1.0,
        "score_trend": score_trend
    }

