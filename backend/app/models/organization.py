from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, default="university") # "university", "company"

    cohorts = relationship("Cohort", back_populates="organization", cascade="all, delete-orphan")


class Cohort(Base):
    __tablename__ = "cohorts"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False) # e.g. "AI & Data Science - 2026 Batch"
    branch = Column(String, default="")
    graduation_year = Column(Integer, default=2026)

    organization = relationship("Organization", back_populates="cohorts")
    profiles = relationship("Profile", back_populates="cohort")

