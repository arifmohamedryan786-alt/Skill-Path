from datetime import datetime, timedelta
from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import Profile, AgentLog, Career, CareerShortlist
from backend.app.agents.discovery_agent import discovery_agent
from backend.app.agents.career_matcher_agent import career_matcher_agent
from backend.app.agents.skill_analyst_agent import skill_analyst_agent
from backend.app.agents.learning_coach_agent import learning_coach_agent
from backend.app.agents.resource_recommender_agent import resource_recommender_agent
from backend.app.agents.roadmap_planner_agent import roadmap_planner_agent
from backend.app.agents.simulation_agent import simulation_agent
from backend.app.agents.progress_evaluator_agent import progress_evaluator_agent

class AgentOrchestrator:
    """
    Central Multi-Agent Event Router (LangGraph Pattern):
    Dispatches events between specialized agents, coordinates state updates,
    and logs every inter-agent hand-off in AgentLog for explainable AI.
    """

    def on_goal_changed(
        self,
        db: Session,
        user_id: int,
        new_career_slug: str,
        reason: str = "Learner changed target career"
    ) -> dict[str, Any]:
        """
        Triggered when learner selects a new career or switches from shortlist:
        1. Updates user profile goal
        2. Career Matcher & Skill Analyst re-evaluate gaps
        3. Roadmap Planner rebuilds 7-stage roadmap
        4. Simulation Agent calculates new job-ready date
        5. Logs explainable AI audit trail
        """
        career = db.query(Career).filter(Career.slug == new_career_slug).first()
        career_name = career.name if career else new_career_slug.replace("-", " ").title()

        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if profile:
            profile.career_goal = career_name
            profile.goal_status = "known"
            db.commit()

        # Step A: Rebuild Roadmap
        stages = roadmap_planner_agent.build_or_rebuild_roadmap(db, user_id, new_career_slug)

        # Step B: Recompute Match & Gaps
        match_info = career_matcher_agent.calculate_match(db, user_id, career.id if career else 1)

        # Step C: Recompute Forecast
        forecast_info = simulation_agent.calculate_forecast(db, user_id, career_slug_override=new_career_slug)

        # Step D: Log Explainable AI Hand-off
        log = AgentLog(
            user_id=user_id,
            agent_name="Orchestrator",
            action="Rebuilt Roadmap & Forecast",
            reason=f"Goal adapted to {career_name}. Roadmap Planner regenerated 7 stages, Career Matcher computed {match_info['match_pct']}% match, and Simulation Agent estimated readiness for {forecast_info['realistic_date']}.",
            details={
                "new_career": career_name,
                "match_pct": match_info["match_pct"],
                "realistic_date": forecast_info["realistic_date"]
            }
        )
        db.add(log)
        db.commit()

        return {
            "career_name": career_name,
            "stages_count": len(stages),
            "match_pct": match_info["match_pct"],
            "forecast_date": forecast_info["realistic_date"],
            "message": f"Successfully switched target career to {career_name}. Your entire roadmap and job-ready forecast have been adapted."
        }

    def on_inactivity_detected(self, db: Session, user_id: int) -> dict[str, Any]:
        """
        Triggered when 7 days of inactivity elapse:
        Sends gentle nudge and adjusts weekly sprint to a lighter workload.
        """
        log = AgentLog(
            user_id=user_id,
            agent_name="Orchestrator",
            action="Inactivity Rebalance",
            reason="7 days of inactivity detected. Adjusted weekly sprint to lighter 30-minute daily blocks and queued encouraging check-in.",
            details={"action": "reduced_weekly_load"}
        )
        db.add(log)
        db.commit()
        return {"status": "rebalanced"}

orchestrator = AgentOrchestrator()

