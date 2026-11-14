from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from backend.app.database import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)       # e.g., "AI/ML Engineer"
    difficulty = Column(String, default="Junior") # "Intern", "Junior", "Mid-level"
    questions = Column(JSON, default=list)      # [{"id": 1, "topic": "Python", "question": "..."}]
    answers = Column(JSON, default=list)        # [{"question_id": 1, "answer_text": "..."}]
    rubric_scores = Column(JSON, default=dict)  # {"correctness": 4, "depth": 3, "clarity": 4, "examples": 3, "overall": 3.5}
    strengths = Column(JSON, default=list)      # ["Clear explanation of data types", ...]
    mistakes = Column(JSON, default=list)       # ["Missed indexing complexity", ...]
    sample_answers = Column(JSON, default=list) # [{"question_id": 1, "ideal_answer": "..."}]
    practice_items = Column(JSON, default=list) # [{"skill": "Python", "task": "Practice time complexity problems"}]
    weak_skills = Column(JSON, default=list)    # ["Statistics", "SQL"]
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interviews")

