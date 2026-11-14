from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import UserSkill, Skill, Career, CareerSkill

class SkillAnalystAgent:
    """
    Analyzes all skills across the user's profile, organizes them by category,
    identifies top strengths and critical blind spots, and prepares radar chart data.
    """

    def analyze_user_skills(self, db: Session, user_id: int, target_career_slug: str = "") -> dict[str, Any]:
        user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
        user_skills_dict = {us.skill_id: us for us in user_skills}

        # Categories for radar chart
        categories = ["Programming", "Data", "AI", "Web", "Cloud", "Testing", "Design"]
        category_levels = {cat: {"total_level": 0.0, "count": 0} for cat in categories}

        all_skills = db.query(Skill).all()
        skill_details = []
        strengths = []
        weaknesses = []

        for sk in all_skills:
            usk = user_skills_dict.get(sk.id)
            level = usk.level if usk else 0
            conf = usk.confidence if usk else 0.0

            item = {
                "skill_id": sk.id,
                "name": sk.name,
                "slug": sk.slug,
                "category": sk.category,
                "level": level,
                "confidence": conf,
                "source": usk.source if usk else "none"
            }
            skill_details.append(item)

            # Update category averages
            if sk.category in category_levels and level > 0:
                category_levels[sk.category]["total_level"] += level
                category_levels[sk.category]["count"] += 1

            if level >= 2:
                strengths.append(item)
            elif level == 0 or level == 1:
                weaknesses.append(item)

        # Radar chart points (scale 0 to 100)
        radar_points = []
        for cat in categories:
            data = category_levels[cat]
            avg_lvl = (data["total_level"] / max(data["count"], 1)) if data["count"] > 0 else 0.0
            # Scale level 0-4 to 0-100%
            pct = round((avg_lvl / 4.0) * 100.0, 1) if data["count"] > 0 else 10.0
            radar_points.append({
                "subject": cat,
                "current": pct,
                "target": 80.0
            })

        # Sort strengths and weaknesses
        strengths.sort(key=lambda x: x["level"], reverse=True)

        return {
            "radar_chart": radar_points,
            "strengths": strengths[:6],
            "weaknesses": weaknesses[:8],
            "total_assessed_skills": len([s for s in skill_details if s["level"] > 0]),
            "overall_competency_tier": "Intermediate" if len(strengths) >= 4 else "Foundational Beginner"
        }

skill_analyst_agent = SkillAnalystAgent()

