from typing import Optional, Any
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    role: str = "assistant"
    content: str
    reply: Optional[str] = None
    suggested_chips: list[str] = []
    tool_executed: Optional[str] = None
    tool_data: Optional[dict[str, Any]] = None
    ai_busy: Optional[bool] = False

class MentorFeedbackRequest(BaseModel):
    message_id: int
    feedback: str # "helpful", "unhelpful"
    notes: Optional[str] = None

