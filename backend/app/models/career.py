from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    plain_description = Column(String, nullable=False)
    day_in_life = Column(String, nullable=False)
    typical_tasks = Column(JSON, default=list) # ["Write queries to pull sales data", ...]
    entry_titles = Column(JSON, default=list)  # ["Junior Data Analyst", "Associate BI Analyst"]
    growth_path = Column(JSON, default=list)   # ["Junior (0-2y)", "Mid-level (2-5y)", "Senior/Lead (5y+)"]
    demand_level = Column(String, default="High") # "Very High", "High", "Growing"
    salary_range_note = Column(String, default="₹4.5L - ₹9L / year entry-level (check current market data)")
    suits_who = Column(String, nullable=False)
    mini_project = Column(JSON, default=dict)  # {"title": "...", "duration": "1 hour", "description": "...", "steps": [...]}

    career_skills = relationship("CareerSkill", back_populates="career", cascade="all, delete-orphan")
    shortlists = relationship("CareerShortlist", back_populates="career", cascade="all, delete-orphan")
    forecasts = relationship("ForecastSnapshot", back_populates="career", cascade="all, delete-orphan")


class CareerSkill(Base):
    __tablename__ = "career_skills"

    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    target_level = Column(Integer, default=2) # 1 (Basic), 2 (Working), 3 (Proficient), 4 (Advanced)
    weight = Column(Integer, default=3)       # 1 to 5 priority weight

    career = relationship("Career", back_populates="career_skills")
    skill = relationship("Skill", back_populates="career_skills")


class CareerShortlist(Base):
    __tablename__ = "career_shortlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    is_primary = Column(Boolean, default=False)
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="shortlists")
    career = relationship("Career", back_populates="shortlists")

