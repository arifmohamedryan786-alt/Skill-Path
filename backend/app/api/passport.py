from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.passport import SkillPassport, VerifiedSkill
from backend.app.models.user import User, Profile
from backend.app.models.skill import Skill, UserSkill
from backend.app.models.career import Career
from backend.app.schemas.passport import (
    PassportOut, PassportSettingsUpdate, PassportPublicOut,
    VerifiedSkillOut, VerifyHashResponse
)
from backend.app.api.deps import get_current_user
from backend.app.agents.career_matcher_agent import career_matcher_agent
from backend.app.utils.hashing import verify_skill_hash, compute_verification_hash
from backend.app.utils.pdf_generator import generate_passport_pdf

router = APIRouter(prefix="/passport", tags=["Verified Skill Passport"])

@router.get("", response_model=PassportOut)
def get_user_passport(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    passport = db.query(SkillPassport).filter(SkillPassport.user_id == current_user.id).first()
    if not passport:
        slug = f"user-{current_user.id:04d}"
        passport = SkillPassport(user_id=current_user.id, slug=slug, is_public=True)
        db.add(passport)
        db.commit()
        db.refresh(passport)

    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    target_career = profile.career_goal if profile and profile.career_goal else "AI/ML Engineer"

    # Match %
    career = db.query(Career).filter(Career.name.ilike(f"%{target_career}%")).first()
    match_data = career_matcher_agent.calculate_match(db, current_user.id, career.id) if career else {}
    readiness_pct = match_data.get("match_pct", 0.0)

    # Verified skills
    verified = db.query(VerifiedSkill).filter(VerifiedSkill.passport_id == passport.id).all()
    verified_outs = []
    for vs in verified:
        sk = db.query(Skill).filter(Skill.id == vs.skill_id).first()
        verified_outs.append(VerifiedSkillOut(
            id=vs.id,
            skill_id=vs.skill_id,
            skill_name=sk.name if sk else "Skill",
            category=sk.category if sk else "General",
            verified_level=vs.verified_level,
            score_pct=vs.score_pct,
            evidence_type=vs.evidence_type,
            evidence_ref=vs.evidence_ref,
            verification_hash=vs.verification_hash,
            verified_at=vs.verified_at.strftime("%d %b %Y")
        ))

    # All user skills
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    all_skills_list = []
    for us in user_skills:
        sk = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if sk:
            all_skills_list.append({
                "skill_id": sk.id,
                "name": sk.name,
                "level": us.level,
                "source": us.source
            })

    public_url = f"/passport/{passport.slug}"

    return PassportOut(
        id=passport.id,
        slug=passport.slug,
        full_name=profile.full_name if profile else "Student",
        target_career=target_career,
        readiness_pct=readiness_pct,
        is_public=passport.is_public,
        show_scores=passport.show_scores,
        show_evidence=passport.show_evidence,
        verified_skills=verified_outs,
        all_skills=all_skills_list,
        public_url=public_url,
        qr_data_url=f"https://skillpath.dev{public_url}"
    )

@router.put("", response_model=PassportOut)
def update_passport_settings(
    settings_in: PassportSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    passport = db.query(SkillPassport).filter(SkillPassport.user_id == current_user.id).first()
    if not passport:
        raise HTTPException(status_code=404, detail="Passport not found")

    if settings_in.is_public is not None:
        passport.is_public = settings_in.is_public
    if settings_in.show_scores is not None:
        passport.show_scores = settings_in.show_scores
    if settings_in.show_evidence is not None:
        passport.show_evidence = settings_in.show_evidence

    db.commit()
    db.refresh(passport)
    return get_user_passport(current_user=current_user, db=db)

@router.get("/public/{slug}", response_model=PassportPublicOut)
def get_public_passport(slug: str, db: Session = Depends(get_db)):
    passport = db.query(SkillPassport).filter(SkillPassport.slug == slug).first()
    if not passport or not passport.is_public:
        raise HTTPException(status_code=404, detail="Public passport profile not found or private")

    user = db.query(User).filter(User.id == passport.user_id).first()
    profile = db.query(Profile).filter(Profile.user_id == passport.user_id).first()
    target_career = profile.career_goal if profile and profile.career_goal else "Tech Professional"

    career = db.query(Career).filter(Career.name.ilike(f"%{target_career}%")).first()
    match_data = career_matcher_agent.calculate_match(db, passport.user_id, career.id) if career else {}

    verified = db.query(VerifiedSkill).filter(VerifiedSkill.passport_id == passport.id).all()
    verified_outs = []
    for vs in verified:
        sk = db.query(Skill).filter(Skill.id == vs.skill_id).first()
        verified_outs.append(VerifiedSkillOut(
            id=vs.id,
            skill_id=vs.skill_id,
            skill_name=sk.name if sk else "Skill",
            category=sk.category if sk else "General",
            verified_level=vs.verified_level,
            score_pct=vs.score_pct if passport.show_scores else 0.0,
            evidence_type=vs.evidence_type if passport.show_evidence else "verified",
            evidence_ref=vs.evidence_ref if passport.show_evidence else "authenticated",
            verification_hash=vs.verification_hash,
            verified_at=vs.verified_at.strftime("%d %b %Y")
        ))

    return PassportPublicOut(
        slug=passport.slug,
        full_name=profile.full_name if profile else "Learner",
        education=profile.education if profile else "",
        branch=profile.branch if profile else "",
        target_career=target_career,
        readiness_pct=match_data.get("match_pct", 0.0),
        verified_skills=verified_outs,
        verified_count=len(verified_outs)
    )

@router.get("/verify/{skill_id}", response_model=VerifyHashResponse)
def verify_skill_fingerprint(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    passport = db.query(SkillPassport).filter(SkillPassport.user_id == current_user.id).first()
    if not passport:
        raise HTTPException(status_code=404, detail="Passport not found")

    vs = db.query(VerifiedSkill).filter(
        VerifiedSkill.passport_id == passport.id,
        VerifiedSkill.skill_id == skill_id
    ).first()

    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    skill_name = skill.name if skill else "Skill"
    skill_slug = skill.slug if skill else ""

    if not vs:
        return VerifyHashResponse(
            skill_name=skill_name,
            is_valid=False,
            stored_hash="none",
            recomputed_hash="none",
            timestamp=datetime.utcnow().isoformat(),
            details="No verified record exists for this skill."
        )

    date_str = vs.verified_at.strftime("%Y-%m-%d")
    recomputed = compute_verification_hash(current_user.id, skill_slug, vs.score_pct, date_str)
    is_valid = (vs.verification_hash == recomputed)

    return VerifyHashResponse(
        skill_name=skill_name,
        is_valid=is_valid,
        stored_hash=vs.verification_hash,
        recomputed_hash=recomputed,
        timestamp=datetime.utcnow().isoformat(),
        details="SHA-256 cryptographic verification succeeded! The record is authentic and unaltered." if is_valid else "Hash mismatch detected! Record integrity failed."
    )

@router.get("/pdf")
def export_passport_pdf(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    passport_data = get_user_passport(current_user=current_user, db=db)
    
    verified_list = [
        {"name": v.skill_name, "level": v.verified_level, "score": v.score_pct, "hash": v.verification_hash}
        for v in passport_data.verified_skills
    ]

    pdf_bytes = generate_passport_pdf(
        student_name=passport_data.full_name,
        target_career=passport_data.target_career,
        readiness_pct=passport_data.readiness_pct,
        verified_skills=verified_list,
        public_url=f"https://skillpath.dev{passport_data.public_url}"
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=SkillPath_Passport_{passport_data.slug}.pdf"}
    )

