from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import Career, CareerSkill, UserSkill, Skill

class CareerMatcherAgent:
    """
    Computes exact weighted match percentage and gap analysis for a target career:
    match % = sum(min(current_level, target_level) * weight) / sum(target_level * weight)
    """

    def calculate_match(
        self,
        db: Session,
        user_id: int,
        career_id: int
    ) -> dict[str, Any]:
        career = db.query(Career).filter(Career.id == career_id).first()
        if not career:
            return {
                "match_pct": 0.0,
                "readiness_label": "Not Found",
                "total_skills": 0,
                "matched_count": 0,
                "gaps": [],
                "strengths": []
            }

        career_skills = db.query(CareerSkill).filter(CareerSkill.career_id == career_id).all()
        user_skills_map = {
            us.skill_id: us.level
            for us in db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
        }

        total_target_weight = 0.0
        current_earned_weight = 0.0

        gaps = []
        strengths = []

        for cs in career_skills:
            target = cs.target_level
            weight = cs.weight
            total_target_weight += target * weight

            cur_level = user_skills_map.get(cs.skill_id, 0)
            earned = min(cur_level, target)
            current_earned_weight += earned * weight

            skill_rec = db.query(Skill).filter(Skill.id == cs.skill_id).first()
            skill_name = skill_rec.name if skill_rec else f"Skill #{cs.skill_id}"
            skill_slug = skill_rec.slug if skill_rec else ""
            category = skill_rec.category if skill_rec else "General"

            item_info = {
                "skill_id": cs.skill_id,
                "slug": skill_slug,
                "name": skill_name,
                "category": category,
                "current_level": cur_level,
                "target_level": target,
                "weight": weight,
                "gap": max(0, target - cur_level)
            }

            if cur_level >= target and cur_level > 0:
                strengths.append(item_info)
            elif cur_level < target:
                gaps.append(item_info)

        match_pct = (current_earned_weight / total_target_weight * 100.0) if total_target_weight > 0 else 0.0
        match_pct = round(match_pct, 1)

        # Readiness label
        if match_pct >= 80.0:
            readiness_label = "Job Ready (Interview Stage)"
        elif match_pct >= 60.0:
            readiness_label = "Portfolio Builder (Project Ready)"
        elif match_pct >= 30.0:
            readiness_label = "Active Learner (Core Skills Stage)"
        else:
            readiness_label = "Beginning Explorer (Foundations Stage)"

        # Sort gaps by weight (highest priority first)
        gaps.sort(key=lambda x: (x["weight"], x["gap"]), reverse=True)

        return {
            "career_id": career.id,
            "career_name": career.name,
            "match_pct": match_pct,
            "readiness_label": readiness_label,
            "total_skills": len(career_skills),
            "matched_count": len(strengths),
            "gaps_count": len(gaps),
            "gaps": gaps,
            "strengths": strengths
        }

career_matcher_agent = CareerMatcherAgent()

