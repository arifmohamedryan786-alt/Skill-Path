from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.database import Base

class PracticeQuestion(Base):
    __tablename__ = "practice_questions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)          # e.g. "Python", "DSA", "C Programming"
    category_slug = Column(String, nullable=False, index=True)     # e.g. "python", "dsa", "c-programming"
    title = Column(String, nullable=False)
    difficulty = Column(String, nullable=False, index=True)        # "Beginner", "Intermediate", "Advanced"
    description = Column(Text, nullable=False)
    example_input = Column(Text, default="")
    example_output = Column(Text, default="")
    hint = Column(Text, default="")
    starter_code = Column(Text, default="")
    solution = Column(Text, default="")
    explanation = Column(Text, default="")
    approach = Column(Text, default="")
    time_complexity = Column(String, default="O(N)")
    space_complexity = Column(String, default="O(1)")
    order_index = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    progress_entries = relationship("PracticeProgress", back_populates="question", cascade="all, delete-orphan")


class PracticeProgress(Base):
    __tablename__ = "practice_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("practice_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String, default="not_started")                  # "not_started", "attempted", "completed"
    solution_code = Column(Text, default="")
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="practice_progress")
    question = relationship("PracticeQuestion", back_populates="progress_entries")

