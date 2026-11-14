from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.skill import Skill, UserSkill
from backend.app.models.user import User, Profile
from backend.app.api.deps import get_current_user
from backend.app.agents.learning_coach_agent import learning_coach_agent

router = APIRouter(prefix="/skills", tags=["Skills & Learning Coach"])

@router.get("/{skill_id}/how-to-learn")
def get_how_to_learn_card(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    weekly_hours = profile.weekly_hours if profile else 8.0
    career_goal = profile.career_goal if profile else ""

    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_id == skill_id
    ).first()
    current_lvl = user_skill.level if user_skill else 0

    card = learning_coach_agent.generate_how_to_learn_card(
        db=db,
        skill_id=skill_id,
        user_weekly_hours=weekly_hours,
        user_current_level=current_lvl,
        career_goal=career_goal
    )
    if not card:
        raise HTTPException(status_code=404, detail="Skill not found")
    return card

