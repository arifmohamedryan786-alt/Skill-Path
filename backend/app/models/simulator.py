from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, default="Custom Scenario")
    target_career = Column(String, default="")
    weekly_hours = Column(Float, default=8.0)
    pace_factor = Column(Float, default=1.0)
    simulated_skills = Column(JSON, default=dict) # {skill_slug: simulated_level}
    ready_date = Column(String, default="")
    match_pct_4w = Column(Float, default=0.0)
    match_pct_8w = Column(Float, default=0.0)
    match_pct_12w = Column(Float, default=0.0)
    explanation = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="scenarios")


class ForecastSnapshot(Base):
    __tablename__ = "forecast_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="CASCADE"), nullable=True)
    total_hours_needed = Column(Float, default=0.0)
    weekly_hours = Column(Float, default=8.0)
    pace_factor = Column(Float, default=1.0)
    current_match_pct = Column(Float, default=0.0)
    optimistic_weeks = Column(Integer, default=12)
    realistic_weeks = Column(Integer, default=16)
    optimistic_date = Column(String, default="")
    realistic_date = Column(String, default="")
    explanation = Column(String, default="")
    calculated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="forecasts")
    career = relationship("Career", back_populates="forecasts")

