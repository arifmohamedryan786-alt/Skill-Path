from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from backend.app.database import Base

class DiscoveryResponse(Base):
    __tablename__ = "discovery_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    answers = Column(JSON, default=dict)       # {question_id: answer_val}
    aptitude_scores = Column(JSON, default=dict) # {"analytical": 85, "creative": 60, "technical": 90, ...}
    top_careers = Column(JSON, default=list)    # [{"career_id": 1, "name": "AI/ML Engineer", "match_pct": 92, "reason": "..."}]
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="discovery_responses")

