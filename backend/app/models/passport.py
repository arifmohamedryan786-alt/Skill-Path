from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class SkillPassport(Base):
    __tablename__ = "skill_passports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False) # e.g. "arif-mohamed-8a9d"
    is_public = Column(Boolean, default=True)
    show_scores = Column(Boolean, default=True)
    show_evidence = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="passport")
    verified_skills = relationship("VerifiedSkill", back_populates="passport", cascade="all, delete-orphan")


class VerifiedSkill(Base):
    __tablename__ = "verified_skills"

    id = Column(Integer, primary_key=True, index=True)
    passport_id = Column(Integer, ForeignKey("skill_passports.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    verified_level = Column(Integer, default=1)
    score_pct = Column(Float, nullable=False)
    evidence_type = Column(String, default="assessment") # "assessment" or "project"
    evidence_ref = Column(String, default="")           # Assessment ID or Project URL
    verification_hash = Column(String, nullable=False)  # SHA-256 of (user_id, skill_slug, score_pct, date_str)
    verified_at = Column(DateTime, default=datetime.utcnow)

    passport = relationship("SkillPassport", back_populates="verified_skills")
    skill = relationship("Skill", back_populates="verified_skills")

