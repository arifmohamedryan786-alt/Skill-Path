from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    target_level = Column(Integer, default=1) # The level being tested (e.g. 1 to 4)
    # questions format: list of 5 MCQs + 1 practical task
    # [{ "id": 1, "type": "mcq", "question": "...", "options": ["A", "B", "C", "D"], "correct_index": 0, "explanation": "..." }]
    questions = Column(JSON, default=list)
    practical_task = Column(JSON, default=dict) # {"prompt": "...", "hint": "...", "evaluation_criteria": "..."}

    skill = relationship("Skill", back_populates="assessments")
    results = relationship("AssessmentResult", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    score_pct = Column(Float, nullable=False) # e.g. 82.0
    passed = Column(Boolean, default=False)   # >= 70% is passed
    mcq_answers = Column(JSON, default=dict)  # {question_id: selected_index}
    practical_submission = Column(String, default="")
    feedback = Column(JSON, default=dict)     # {"summary": "...", "strengths": [...], "remedial_topics": [...]}
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessment_results")
    assessment = relationship("Assessment", back_populates="results")

