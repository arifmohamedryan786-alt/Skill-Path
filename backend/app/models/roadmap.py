from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class RoadmapStage(Base):
    __tablename__ = "roadmap_stages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    stage_number = Column(Integer, nullable=False) # 1 to 7
    title = Column(String, nullable=False) # e.g. "1 Explore", "2 Foundations", "3 Core skills", "4 Projects", "5 Internships", "6 Interview prep", "7 Growth"
    description = Column(String, nullable=False)
    status = Column(String, default="locked") # "completed", "current", "locked"
    est_weeks = Column(Integer, default=4)

    user = relationship("User", back_populates="roadmap_stages")
    items = relationship("RoadmapItem", back_populates="stage", cascade="all, delete-orphan", order_by="RoadmapItem.order")


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("roadmap_stages.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="SET NULL"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    item_type = Column(String, default="skill") # "skill", "project", "milestone", "internship", "certification", "remedial"
    order = Column(Integer, default=1)
    status = Column(String, default="pending") # "pending", "in_progress", "completed", "skipped"
    due_week = Column(Integer, default=1)
    est_hours = Column(Float, default=10.0)
    completed_at = Column(DateTime, nullable=True)

    stage = relationship("RoadmapStage", back_populates="items")
    user = relationship("User", back_populates="roadmap_items")


class WeeklySprint(Base):
    __tablename__ = "weekly_sprints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    week_number = Column(Integer, default=1)
    title = Column(String, default="Week 1: Foundations")
    focus_summary = Column(String, default="")
    target_hours = Column(Float, default=8.0)
    tasks = Column(JSON, default=list) # [{"id": 1, "task": "...", "duration_mins": 45, "completed": False, "day": "Monday"}]
    status = Column(String, default="active") # "active", "completed", "missed"
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="sprints")

