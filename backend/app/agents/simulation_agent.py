import math
from datetime import datetime, timedelta
from typing import Any, Optional
from sqlalchemy.orm import Session
from backend.app.models import (
    Career, CareerSkill, UserSkill, Skill, Profile, ForecastSnapshot, Scenario, AgentLog
)
from backend.app.agents.career_matcher_agent import career_matcher_agent

class SimulationAgent:
    """
    Flight Simulator Agent:
    Predicts time to job readiness using the exact mathematical formula:
    hours_needed = (target_level - current_level) * estimated_hours_per_level * difficulty * learner_pace_factor
    weeks = total_hours / weekly_hours
    Generates optimistic and realistic milestone dates, what-if projections, and plain explanations.
    """

    def calculate_forecast(
        self,
        db: Session,
        user_id: int,
        career_slug_override: Optional[str] = None,
        weekly_hours_override: Optional[float] = None,
        simulated_skill_levels: Optional[dict[str, int]] = None,
        simulate_fail: bool = False
    ) -> dict[str, Any]:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        career_slug = career_slug_override or (profile.career_goal if profile and profile.career_goal else "ai-ml-engineer")
        weekly_hours = weekly_hours_override if weekly_hours_override is not None else (profile.weekly_hours if profile else 8.0)
        pace_factor = profile.learner_pace_factor if profile else 1.0

        if simulate_fail:
            pace_factor = round(pace_factor * 1.25, 2)

        career = db.query(Career).filter(Career.slug == career_slug).first()
        if not career:
            career = db.query(Career).first()

        career_skills = db.query(CareerSkill).filter(CareerSkill.career_id == career.id).all()
        user_skills_map = {
            us.skill_id: us.level
            for us in db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
        }

        # Apply simulated skill levels if provided
        simulated_levels = simulated_skill_levels or {}

        total_hours_needed = 0.0
        gaps_count = 0

        for cs in career_skills:
            skill = db.query(Skill).filter(Skill.id == cs.skill_id).first()
            if not skill:
                continue

            # Check simulated level by slug or fallback to actual level
            current_lvl = simulated_levels.get(skill.slug, user_skills_map.get(skill.id, 0))
            target_lvl = cs.target_level

            if current_lvl < target_lvl:
                gaps_count += 1
                diff = target_lvl - current_lvl
                base_hrs = skill.estimated_hours_per_level
                diff_mult = skill.difficulty
                hours_for_skill = diff * base_hrs * diff_mult * pace_factor
                total_hours_needed += hours_for_skill

        weeks_needed = max(1, math.ceil(total_hours_needed / max(weekly_hours, 1.0)))

        # Optimistic (fast execution, 85% of time) vs Realistic (115% of time with buffer)
        optimistic_weeks = max(1, math.ceil(weeks_needed * 0.85))
        realistic_weeks = max(1, math.ceil(weeks_needed * 1.15))

        today = datetime.utcnow()
        opt_date = today + timedelta(weeks=optimistic_weeks)
        real_date = today + timedelta(weeks=realistic_weeks)

        opt_date_str = opt_date.strftime("%d %B %Y")
        real_date_str = real_date.strftime("%d %B %Y")

        # Current match percentage
        match_info = career_matcher_agent.calculate_match(db, user_id, career.id)
        current_match = match_info["match_pct"]

        # Calculate projected match % at week 4, 8, 12
        def project_match(at_week: int) -> float:
            fraction = min(at_week / max(weeks_needed, 1), 1.0)
            return round(min(current_match + ((100.0 - current_match) * fraction), 100.0), 1)

        m_4w = project_match(4)
        m_8w = project_match(8)
        m_12w = project_match(12)

        projection_points = [
            {"week": 0, "match": current_match, "label": "Today"},
            {"week": 4, "match": m_4w, "label": "Week 4"},
            {"week": 8, "match": m_8w, "label": "Week 8"},
            {"week": 12, "match": m_12w, "label": "Week 12"},
            {"week": realistic_weeks, "match": 100.0, "label": "Job Ready"}
        ]

        explanation = (
            f"At your current study pace of {weekly_hours:.0f} hours/week (pace factor {pace_factor:.2f}), "
            f"you have approximately {round(total_hours_needed)} hours of focused learning remaining. "
            f"You will reach job readiness between {opt_date_str} (optimistic) and {real_date_str} (realistic)."
        )

        return {
            "career_goal": career.name,
            "career_slug": career.slug,
            "current_match_pct": current_match,
            "total_gap_hours": round(total_hours_needed, 1),
            "weekly_hours": weekly_hours,
            "learner_pace_factor": pace_factor,
            "optimistic_date": opt_date_str,
            "realistic_date": real_date_str,
            "optimistic_weeks": optimistic_weeks,
            "realistic_weeks": realistic_weeks,
            "weeks_needed": weeks_needed,
            "match_pct_4w": m_4w,
            "match_pct_8w": m_8w,
            "match_pct_12w": m_12w,
            "projection_points": projection_points,
            "readiness_label": match_info["readiness_label"],
            "explanation": explanation,
            "gaps_count": gaps_count
        }

    def save_and_apply_scenario(
        self,
        db: Session,
        user_id: int,
        weekly_hours: float,
        target_career_slug: Optional[str] = None
    ) -> dict[str, Any]:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if profile:
            profile.weekly_hours = weekly_hours
            if target_career_slug:
                profile.career_goal = target_career_slug.replace("-", " ").title()
            db.commit()

        # Log Explainable AI plan application
        log = AgentLog(
            user_id=user_id,
            agent_name="Simulation Agent",
            action="Applied Scenario Plan",
            reason=f"Applied updated weekly schedule of {weekly_hours} hours/week to your roadmap and recalculated all stage completion targets.",
            details={"weekly_hours": weekly_hours, "target_career": target_career_slug}
        )
        db.add(log)
        db.commit()

        return self.calculate_forecast(db, user_id, career_slug_override=target_career_slug, weekly_hours_override=weekly_hours)

simulation_agent = SimulationAgent()

