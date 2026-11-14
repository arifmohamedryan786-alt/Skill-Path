from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import asyncio
import json
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.agent_log import ChatMessage
from backend.app.schemas.mentor import ChatRequest, ChatResponse, MentorFeedbackRequest
from backend.app.api.deps import get_current_user
from backend.app.agents.ai_mentor_agent import ai_mentor_agent

router = APIRouter(prefix="/mentor", tags=["AI Mentor"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_mentor(
    chat_req: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    res = await ai_mentor_agent.generate_response(db, current_user.id, chat_req.message)
    res["reply"] = res.get("content", "")
    return res

@router.get("/history")
def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.created_at.asc()).all()

    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "created_at": m.created_at.strftime("%I:%M %p"),
            "metadata": m.metadata_json or {}
        }
        for m in messages
    ]

@router.post("/feedback")
def submit_mentor_feedback(
    fb_req: MentorFeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    msg = db.query(ChatMessage).filter(ChatMessage.id == fb_req.message_id).first()
    if msg:
        meta = dict(msg.metadata_json or {})
        meta["feedback"] = fb_req.feedback
        meta["feedback_notes"] = fb_req.notes
        msg.metadata_json = meta
        db.commit()
    return {"status": "Feedback recorded, thank you!"}

