from datetime import datetime, timedelta
from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import (
    User, Profile, AssessmentResult, RoadmapItem, AgentLog
)

class ProgressEvaluatorAgent:
    """
    Monitors learning velocity, assessment scores, and completion timestamps.
    Dynamically recalculates learner_pace_factor:
    - Faster completion & high scores (>80%) -> pace_factor decreases (e.g. 0.85, faster pace)
    - Slower completion & struggles (<50%) -> pace_factor increases (e.g. 1.25, needs more time)
    """

    def evaluate_pace_factor(self, db: Session, user_id: int) -> float:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            return 1.0

        results = db.query(AssessmentResult).filter(AssessmentResult.user_id == user_id).all()
        if not results:
            return profile.learner_pace_factor

        avg_score = sum(r.score_pct for r in results) / len(results)

        # Base multiplier
        if avg_score >= 85.0:
            new_pace = 0.85  # 15% faster than average
        elif avg_score >= 70.0:
            new_pace = 0.95
        elif avg_score >= 50.0:
            new_pace = 1.10
        else:
            new_pace = 1.30  # Needs 30% more time

        # Smooth update with previous pace
        old_pace = profile.learner_pace_factor
        updated_pace = round((old_pace * 0.4) + (new_pace * 0.6), 2)
        profile.learner_pace_factor = updated_pace
        db.commit()

        # Log change if significant
        if abs(updated_pace - old_pace) >= 0.1:
            log = AgentLog(
                user_id=user_id,
                agent_name="Progress Evaluator Agent",
                action="Updated Pace Factor",
                reason=f"Recalculated learning velocity factor from {old_pace} to {updated_pace} based on recent test average of {avg_score:.1f}%.",
                details={"old_pace": old_pace, "new_pace": updated_pace, "avg_score": avg_score}
            )
            db.add(log)
            db.commit()

        return updated_pace

progress_evaluator_agent = ProgressEvaluatorAgent()

