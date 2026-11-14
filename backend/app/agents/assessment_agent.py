from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import (
    Assessment, AssessmentResult, UserSkill, Skill,
    SkillPassport, VerifiedSkill, RoadmapItem, AgentLog, Profile
)
from backend.app.utils.hashing import compute_verification_hash

class AssessmentAgent:
    """
    Manages generation, grading, adaptive level updating, and verified credential
    creation for skill checkpoint assessments.
    """

    def grade_assessment(
        self,
        db: Session,
        user_id: int,
        assessment_id: int,
        mcq_answers: dict[int, int],
        practical_submission: str = ""
    ) -> dict[str, Any]:
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if not assessment:
            raise ValueError("Assessment not found.")

        skill = db.query(Skill).filter(Skill.id == assessment.skill_id).first()
        questions = assessment.questions or []
        
        # Grade MCQs
        correct_count = 0
        total_mcqs = len(questions)
        remedial_topics = []

        for q in questions:
            q_id = q["id"]
            correct_idx = q.get("correct_index", 0)
            user_idx = mcq_answers.get(q_id, mcq_answers.get(str(q_id), -1))
            if user_idx == correct_idx:
                correct_count += 1
            else:
                remedial_topics.append(q.get("explanation", "Review core concept"))

        # Base MCQ score %
        mcq_pct = (correct_count / total_mcqs * 100.0) if total_mcqs > 0 else 0.0

        # Practical bonus (if code submitted)
        practical_bonus = 0.0
        if practical_submission and len(practical_submission.strip()) > 20:
            practical_bonus = 5.0 # Partial effort boost

        final_score = min(round(mcq_pct + practical_bonus, 1), 100.0)
        passed = final_score >= 70.0

        # Save AssessmentResult
        result = AssessmentResult(
            user_id=user_id,
            assessment_id=assessment_id,
            skill_id=skill.id,
            score_pct=final_score,
            passed=passed,
            mcq_answers=mcq_answers,
            practical_submission=practical_submission,
            feedback={
                "correct_count": correct_count,
                "total": total_mcqs,
                "remedial_topics": remedial_topics
            }
        )
        db.add(result)
        db.flush()

        # Fetch or create UserSkill
        user_skill = db.query(UserSkill).filter(
            UserSkill.user_id == user_id,
            UserSkill.skill_id == skill.id
        ).first()

        if not user_skill:
            user_skill = UserSkill(
                user_id=user_id,
                skill_id=skill.id,
                level=0,
                confidence=0.5,
                source="assessment"
            )
            db.add(user_skill)
            db.flush()

        verification_hash = None
        status_label = ""
        next_action = ""

        # --- ADAPTIVE RULES IMPLEMENTATION ---
        if final_score >= 70.0:
            # Score >= 70%: Mastered! Update level, issue verified badge, unlock roadmap
            user_skill.level = max(user_skill.level, assessment.target_level)
            user_skill.confidence = 0.95
            user_skill.source = "assessment"
            status_label = "Verified Mastered"
            next_action = f"Congratulations! You scored {final_score}%. A verified credential badge has been added to your Skill Passport."

            # Issue VerifiedSkill with SHA-256 tamper-evident hash
            passport = db.query(SkillPassport).filter(SkillPassport.user_id == user_id).first()
            if passport:
                # Remove prior duplicate verification if any
                db.query(VerifiedSkill).filter(
                    VerifiedSkill.passport_id == passport.id,
                    VerifiedSkill.skill_id == skill.id
                ).delete()
                
                date_str = datetime.utcnow().strftime("%Y-%m-%d")
                verification_hash = compute_verification_hash(user_id, skill.slug, final_score, date_str)

                verified_skill = VerifiedSkill(
                    passport_id=passport.id,
                    skill_id=skill.id,
                    verified_level=assessment.target_level,
                    score_pct=final_score,
                    evidence_type="assessment",
                    evidence_ref=f"Assessment #{assessment.id}",
                    verification_hash=verification_hash,
                    verified_at=datetime.utcnow()
                )
                db.add(verified_skill)

            # Update roadmap item status to completed
            roadmap_items = db.query(RoadmapItem).filter(
                RoadmapItem.user_id == user_id,
                RoadmapItem.skill_id == skill.id
            ).all()
            for r_item in roadmap_items:
                r_item.status = "completed"
                r_item.completed_at = datetime.utcnow()

            # Log Explainable AI adaptation
            log = AgentLog(
                user_id=user_id,
                agent_name="Assessment Agent",
                action="Verified Mastery",
                reason=f"Passed {skill.name} assessment with {final_score}% (>= 70%). Promoted to Level {assessment.target_level} and issued cryptographic verified badge.",
                details={"score": final_score, "level": assessment.target_level}
            )
            db.add(log)

        elif final_score >= 50.0:
            # Score 50-69%: Partial progress (+1 level if level 0), schedule retake
            if user_skill.level < 1:
                user_skill.level = 1
            user_skill.confidence = 0.65
            status_label = "Partial Progress"
            next_action = f"Good effort! You scored {final_score}%. You've earned partial credit (Level 1). Review the incorrect questions below and retake the checkpoint when ready."

            log = AgentLog(
                user_id=user_id,
                agent_name="Assessment Agent",
                action="Partial Credit Granted",
                reason=f"Scored {final_score}% on {skill.name} (50-69%). Awarded Level 1 partial credit and suggested targeted revision.",
                details={"score": final_score}
            )
            db.add(log)

        else:
            # Score < 50%: Remedial needed
            status_label = "Remedial Needed"
            next_action = f"You scored {final_score}%. Don't worry at all—this is part of learning! Remedial tutorials have been inserted to help you build confidence before retaking."

            # Insert a remedial roadmap task
            existing_remedial = db.query(RoadmapItem).filter(
                RoadmapItem.user_id == user_id,
                RoadmapItem.item_type == "remedial",
                RoadmapItem.skill_id == skill.id
            ).first()

            if not existing_remedial:
                remedial_item = RoadmapItem(
                    stage_id=1,  # early stage
                    user_id=user_id,
                    skill_id=skill.id,
                    title=f"Remedial Practice: {skill.name} Core Foundations",
                    description=f"Focused 45-minute refresher covering: {', '.join(remedial_topics[:2])}.",
                    item_type="remedial",
                    order=1,
                    status="in_progress",
                    due_week=1,
                    est_hours=3.0
                )
                db.add(remedial_item)

            log = AgentLog(
                user_id=user_id,
                agent_name="Assessment Agent",
                action="Inserted Remedial Item",
                reason=f"Scored {final_score}% (< 50%) on {skill.name}. Inserted remedial foundations item and scheduled encouragement check-in with AI Mentor.",
                details={"score": final_score, "topics": remedial_topics[:2]}
            )
            db.add(log)

        db.commit()

        return {
            "result_id": result.id,
            "skill_id": skill.id,
            "skill_name": skill.name,
            "score_pct": final_score,
            "passed": passed,
            "status_label": status_label,
            "correct_count": correct_count,
            "total_mcqs": total_mcqs,
            "feedback_summary": next_action,
            "remedial_topics": remedial_topics,
            "next_action": next_action,
            "updated_level": user_skill.level,
            "verification_hash": verification_hash
        }

assessment_agent = AssessmentAgent()

