from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, Profile
from backend.app.models.organization import Cohort, Organization
from backend.app.models.skill import UserSkill, Skill
from backend.app.models.agent_log import AgentLog
from backend.app.models.career import Career
from backend.app.api.deps import get_current_admin, get_current_user

router = APIRouter(tags=["Admin & Institutional Analytics"])

@router.get("/admin/cohort-gaps")
def get_cohort_gaps(
    cohort_id: int = 1,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    # Exclude any guest users from cohort calculations
    guest_subquery = db.query(User.id).filter(User.email.like("guest_%@guest.skillpath.dev")).subquery()
    profiles = db.query(Profile).filter(
        Profile.cohort_id == cohort_id,
        ~Profile.user_id.in_(guest_subquery)
    ).all() if cohort else []

    student_count = len(profiles)
    all_skills = db.query(Skill).all()

    # Calculate skill frequency and average level
    skill_stats = []
    for sk in all_skills[:12]:
        levels = []
        for p in profiles:
            usk = db.query(UserSkill).filter(
                UserSkill.user_id == p.user_id,
                UserSkill.skill_id == sk.id
            ).first()
            levels.append(usk.level if usk else 0)

        avg_lvl = sum(levels) / max(len(levels), 1)
        gap_pct = round(max(0.0, (2.5 - avg_lvl) / 2.5 * 100.0), 1)

        skill_stats.append({
            "skill_id": sk.id,
            "skill_name": sk.name,
            "category": sk.category,
            "average_cohort_level": round(avg_lvl, 1),
            "benchmark_target_level": 2.5,
            "cohort_gap_pct": gap_pct
        })

    # Sort by largest gap first
    skill_stats.sort(key=lambda x: x["cohort_gap_pct"], reverse=True)

    return {
        "cohort_id": cohort.id if cohort else 1,
        "cohort_name": cohort.name if cohort else "B.Tech Batch",
        "total_learners": max(student_count, 4),
        "institution": "National Institute of Technology",
        "top_skill_gaps": skill_stats[:6],
        "all_skill_stats": skill_stats
    }

@router.get("/admin/learners")
def get_admin_learners(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    # Only return seeded and registered non-guest learners
    learners = db.query(User).filter(
        User.role == "learner",
        ~User.email.like("guest_%@guest.skillpath.dev")
    ).all()
    results = []
    for u in learners:
        p = db.query(Profile).filter(Profile.user_id == u.id).first()
        results.append({
            "user_id": u.id,
            "email": u.email,
            "full_name": p.full_name if p else "Student",
            "education": p.education if p else "",
            "branch": p.branch if p else "",
            "year": p.year if p else 1,
            "career_goal": p.career_goal if p and p.career_goal else "Not Set",
            "pace_factor": p.learner_pace_factor if p else 1.0,
            "weekly_hours": p.weekly_hours if p else 8.0
        })
    return results

@router.get("/agents/logs")
def get_agent_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logs = db.query(AgentLog).filter(
        AgentLog.user_id == current_user.id
    ).order_by(AgentLog.created_at.desc()).limit(15).all()

    return [
        {
            "id": l.id,
            "agent_name": l.agent_name,
            "action": l.action,
            "reason": l.reason,
            "details": l.details or {},
            "created_at": l.created_at.strftime("%I:%M %p, %d %b")
        }
        for l in logs
    ]

