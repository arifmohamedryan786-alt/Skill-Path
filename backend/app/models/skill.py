from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=False) # e.g. "Programming", "Data", "Web", "AI", "Cloud", "Tools"
    plain_explanation = Column(String, nullable=False)    # Plain English explanation for beginners
    prerequisites = Column(JSON, default=list)            # List of skill names or slugs required first
    estimated_hours_per_level = Column(Float, default=15.0) # Base hours to move up one level
    difficulty = Column(Float, default=1.0)               # Multiplier (e.g. 0.8 easy, 1.0 standard, 1.3 hard)
    common_mistakes = Column(JSON, default=list)          # ["Trying to memorize syntax instead of building", ...]
    done_criteria = Column(JSON, default=list)            # ["Can write a function that filters a list", ...]
    learning_method = Column(JSON, default=dict)          # {"watch_pct": 30, "practice_pct": 50, "build_pct": 20, "tip": "..."}

    career_skills = relationship("CareerSkill", back_populates="skill", cascade="all, delete-orphan")
    user_skills = relationship("UserSkill", back_populates="skill", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="skill", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="skill", cascade="all, delete-orphan")
    verified_skills = relationship("VerifiedSkill", back_populates="skill", cascade="all, delete-orphan")


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    level = Column(Integer, default=0) # 0: None, 1: Basic, 2: Working, 3: Proficient, 4: Advanced
    confidence = Column(Float, default=0.5) # 0.0 - 1.0
    source = Column(String, default="self") # "self", "resume", "assessment", "interview"
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="user_skills")
    skill = relationship("Skill", back_populates="user_skills")

