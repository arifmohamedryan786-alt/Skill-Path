from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, Profile
from backend.app.models.agent_log import AgentLog
from backend.app.schemas.profile import ProfileResponse, ProfileUpdate, ResumeParseRequest, ResumeParseResponse
from backend.app.api.deps import get_current_user
from backend.app.agents.profile_agent import profile_agent
from backend.app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.get("", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id, full_name="Student")
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("", response_model=ProfileResponse)
def update_profile(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    old_goal = profile.career_goal
    update_data = profile_in.model_dump(exclude_unset=True)

    for field, val in update_data.items():
        setattr(profile, field, val)

    db.commit()
    db.refresh(profile)

    # If career goal changed, trigger orchestrator adaptation
    if profile_in.career_goal and profile_in.career_goal != old_goal:
        slug = profile_in.career_goal.lower().replace(" ", "-").replace("/", "-")
        orchestrator.on_goal_changed(db, current_user.id, slug, reason="Profile goal updated by user")

    return profile

@router.post("/resume", response_model=ResumeParseResponse)
async def parse_resume(
    resume_req: ResumeParseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    extracted = await profile_agent.parse_resume(resume_req.resume_text)
    
    # Save log
    log = AgentLog(
        user_id=current_user.id,
        agent_name="Profile Agent",
        action="Parsed Resume",
        reason=f"Extracted {len(extracted.get('extracted_skills', []))} skills from uploaded resume.",
        details=extracted
    )
    db.add(log)
    db.commit()

    return extracted

