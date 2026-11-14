from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from backend.app.database import Base

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    agent_name = Column(String, index=True, nullable=False) # e.g. "Discovery Agent", "Roadmap Planner Agent", etc.
    action = Column(String, nullable=False)                 # e.g. "Ranked Careers", "Rebuilt Roadmap", "Generated Quiz"
    reason = Column(String, nullable=False)                 # Plain language reason
    details = Column(JSON, default=dict)                    # Payload details
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="agent_logs")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False) # "user", "assistant", "system"
    content = Column(String, nullable=False)
    metadata_json = Column(JSON, default=dict) # e.g. {"recommended_resources": [...], "quick_action": "..."}
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_messages")

