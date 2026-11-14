from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.career import Career, CareerSkill, CareerShortlist
from backend.app.models.skill import Skill
from backend.app.models.user import User
from backend.app.schemas.career import (
    CareerOut, CareerDetailOut, CareerCompareRequest, CareerCompareResponse,
    CareerShortlistRequest, CareerShortlistOut, TryItResponse, CareerSkillItem
)
from backend.app.api.deps import get_current_user

router = APIRouter(prefix="/careers", tags=["Careers"])

@router.get("", response_model=list[CareerOut])
def list_careers(db: Session = Depends(get_db)):
    careers = db.query(Career).all()
    return careers

@router.get("/shortlist", response_model=list[CareerShortlistOut])
def get_user_shortlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shortlists = db.query(CareerShortlist).filter(CareerShortlist.user_id == current_user.id).all()
    results = []
    for s in shortlists:
        career = db.query(Career).filter(Career.id == s.career_id).first()
        if career:
            results.append(CareerShortlistOut(
                id=s.id,
                career_id=career.id,
                name=career.name,
                slug=career.slug,
                is_primary=s.is_primary,
                notes=s.notes or "",
                created_at=s.created_at
            ))
    return results

@router.post("/shortlist", response_model=CareerShortlistOut)
def add_to_shortlist(
    shortlist_in: CareerShortlistRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(CareerShortlist).filter(
        CareerShortlist.user_id == current_user.id,
        CareerShortlist.career_id == shortlist_in.career_id
    ).first()

    if existing:
        existing.is_primary = shortlist_in.is_primary or existing.is_primary
        existing.notes = shortlist_in.notes or existing.notes
        db.commit()
        db.refresh(existing)
        s_obj = existing
    else:
        s_obj = CareerShortlist(
            user_id=current_user.id,
            career_id=shortlist_in.career_id,
            is_primary=shortlist_in.is_primary or False,
            notes=shortlist_in.notes or ""
        )
        db.add(s_obj)
        db.commit()
        db.refresh(s_obj)

    career = db.query(Career).filter(Career.id == s_obj.career_id).first()
    return CareerShortlistOut(
        id=s_obj.id,
        career_id=s_obj.career_id,
        name=career.name if career else "",
        slug=career.slug if career else "",
        is_primary=s_obj.is_primary,
        notes=s_obj.notes or "",
        created_at=s_obj.created_at
    )

@router.post("/compare", response_model=CareerCompareResponse)
def compare_careers(
    compare_req: CareerCompareRequest,
    db: Session = Depends(get_db)
):
    selected_careers = db.query(Career).filter(Career.id.in_(compare_req.career_ids)).all()
    if not selected_careers:
        raise HTTPException(status_code=404, detail="No careers found matching provided IDs")

    detailed_careers = []
    skill_sets_by_career: dict[str, set[str]] = {}

    for c in selected_careers:
        c_skills = db.query(CareerSkill).filter(CareerSkill.career_id == c.id).all()
        skill_items = []
        c_set = set()
        for cs in c_skills:
            sk = db.query(Skill).filter(Skill.id == cs.skill_id).first()
            if sk:
                skill_items.append(CareerSkillItem(
                    skill_id=sk.id,
                    name=sk.name,
                    category=sk.category,
                    target_level=cs.target_level,
                    weight=cs.weight,
                    plain_explanation=sk.plain_explanation
                ))
                c_set.add(sk.name)
        skill_sets_by_career[c.name] = c_set

        detailed_careers.append(CareerDetailOut(
            id=c.id,
            slug=c.slug,
            name=c.name,
            plain_description=c.plain_description,
            demand_level=c.demand_level,
            salary_range_note=c.salary_range_note,
            suits_who=c.suits_who,
            entry_titles=c.entry_titles or [],
            day_in_life=c.day_in_life,
            typical_tasks=c.typical_tasks or [],
            growth_path=c.growth_path or [],
            mini_project=c.mini_project or {},
            skills=skill_items
        ))

    # Calculate common skills
    sets_list = list(skill_sets_by_career.values())
    common_skills = list(set.intersection(*sets_list)) if sets_list else []

    # Distinct skills per career
    distinct_skills = {
        name: list(s_set - set(common_skills))
        for name, s_set in skill_sets_by_career.items()
    }

    return CareerCompareResponse(
        careers=detailed_careers,
        common_skills=common_skills,
        distinct_skills=distinct_skills
    )

@router.get("/{career_id}", response_model=CareerDetailOut)
def get_career_details(career_id: int, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")

    c_skills = db.query(CareerSkill).filter(CareerSkill.career_id == career.id).all()
    skill_items = []
    for cs in c_skills:
        sk = db.query(Skill).filter(Skill.id == cs.skill_id).first()
        if sk:
            skill_items.append(CareerSkillItem(
                skill_id=sk.id,
                name=sk.name,
                category=sk.category,
                target_level=cs.target_level,
                weight=cs.weight,
                plain_explanation=sk.plain_explanation
            ))

    return CareerDetailOut(
        id=career.id,
        slug=career.slug,
        name=career.name,
        plain_description=career.plain_description,
        demand_level=career.demand_level,
        salary_range_note=career.salary_range_note,
        suits_who=career.suits_who,
        entry_titles=career.entry_titles or [],
        day_in_life=career.day_in_life,
        typical_tasks=career.typical_tasks or [],
        growth_path=career.growth_path or [],
        mini_project=career.mini_project or {},
        skills=skill_items
    )

@router.get("/{career_id}/try-it", response_model=TryItResponse)
def get_try_it_task(career_id: int, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")

    mp = career.mini_project or {}
    steps = [
        {"step_number": idx + 1, "description": desc}
        for idx, desc in enumerate(mp.get("steps", []))
    ]

    return TryItResponse(
        career_id=career.id,
        career_name=career.name,
        title=mp.get("title", f"Hands-on {career.name} Task"),
        duration=mp.get("duration", "1 hour"),
        summary=mp.get("description", "A bite-sized 1-hour tutorial to experience this career first-hand before committing."),
        steps=steps,
        starter_code=mp.get("starter_code", ""),
        expected_outcome=mp.get("expected_outcome", "A working project ready for your portfolio.")
    )

