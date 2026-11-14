from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, index=True, nullable=False) # "course", "tutorial", "exercise", "project", "book"
    url = Column(String, nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    difficulty = Column(String, default="Beginner") # "Beginner", "Intermediate", "Advanced"
    duration = Column(String, default="2 hours")
    provider = Column(String, default="freeCodeCamp") # "freeCodeCamp", "Khan Academy", "Kaggle", "MDN", "YouTube", etc.
    free = Column(Boolean, default=True)

    skill = relationship("Skill", back_populates="resources")

