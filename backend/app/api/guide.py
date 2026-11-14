from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, Profile
from backend.app.schemas.guide import CareerGuideResponse
from backend.app.api.deps import get_current_user
from backend.app.agents.career_guide_agent import career_guide_agent
from backend.app.utils.pdf_generator import generate_career_guide_pdf

router = APIRouter(prefix="/guide", tags=["Career Guide"])

@router.get("", response_model=CareerGuideResponse)
def get_career_guide(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    guide = career_guide_agent.generate_guide(db, current_user.id)
    return guide

@router.post("/regenerate", response_model=CareerGuideResponse)
def regenerate_guide(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    guide = career_guide_agent.generate_guide(db, current_user.id)
    return guide

@router.get("/pdf")
def export_guide_pdf(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    student_name = profile.full_name if profile else "Student"
    degree_info = f"{profile.education} in {profile.branch}" if profile and profile.branch else "Learner"
    target_career = profile.career_goal if profile and profile.career_goal else "Tech Professional"

    guide = career_guide_agent.generate_guide(db, current_user.id)

    pdf_bytes = generate_career_guide_pdf(
        student_name=student_name,
        degree_info=degree_info,
        target_career=target_career,
        guide_content=guide
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=SkillPath_Guide_{target_career.replace(' ', '_')}.pdf"}
    )

