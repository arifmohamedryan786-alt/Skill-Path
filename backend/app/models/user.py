from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="learner")  # "learner" or "admin"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    user_skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    discovery_responses = relationship("DiscoveryResponse", back_populates="user", cascade="all, delete-orphan")
    shortlists = relationship("CareerShortlist", back_populates="user", cascade="all, delete-orphan")
    roadmap_stages = relationship("RoadmapStage", back_populates="user", cascade="all, delete-orphan")
    roadmap_items = relationship("RoadmapItem", back_populates="user", cascade="all, delete-orphan")
    sprints = relationship("WeeklySprint", back_populates="user", cascade="all, delete-orphan")
    scenarios = relationship("Scenario", back_populates="user", cascade="all, delete-orphan")
    forecasts = relationship("ForecastSnapshot", back_populates="user", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="user", cascade="all, delete-orphan")
    passport = relationship("SkillPassport", back_populates="user", uselist=False, cascade="all, delete-orphan")
    interviews = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    agent_logs = relationship("AgentLog", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    practice_progress = relationship("PracticeProgress", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    education = Column(String, default="")  # e.g., "B.Tech"
    branch = Column(String, default="")     # e.g., "Artificial Intelligence and Data Science"
    year = Column(Integer, default=1)       # 1, 2, 3, 4
    institution = Column(String, default="")
    interests = Column(JSON, default=list)  # ["building", "analyzing data", ...]
    strengths = Column(JSON, default=list)  # ["math", "logical thinking", ...]
    certifications = Column(JSON, default=list)
    projects = Column(JSON, default=list)
    career_goal = Column(String, default="") # e.g. "AI/ML Engineer"
    goal_status = Column(String, default="unknown") # "known", "rough", "unknown"
    weekly_hours = Column(Float, default=8.0)
    language = Column(String, default="en") # "en", "hi", "ta"
    learner_pace_factor = Column(Float, default=1.0)
    cohort_id = Column(Integer, ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")
    cohort = relationship("Cohort", back_populates="profiles")

