from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.interview import InterviewSession
from backend.app.schemas.interview import (
    InterviewStartRequest, InterviewStartResponse, InterviewAnswerRequest,
    InterviewFinishResponse, InterviewSessionOut, InterviewQuestion
)
from backend.app.api.deps import get_current_user
from backend.app.agents.interview_coach_agent import interview_coach_agent

router = APIRouter(prefix="/interview", tags=["Mock Interview Coach"])

@router.post("/start", response_model=InterviewStartResponse)
def start_interview(
    req: InterviewStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    role = req.role or "AI/ML Engineer"
    difficulty = req.difficulty or "Junior"
    session = interview_coach_agent.start_session(db, current_user.id, role=role, difficulty=difficulty)

    return InterviewStartResponse(
        session_id=session.id,
        role=session.role,
        difficulty=session.difficulty,
        questions=[InterviewQuestion(**q) for q in session.questions],
        total_questions=len(session.questions)
    )

@router.post("/answer")
def submit_single_answer(
    ans_req: InterviewAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(InterviewSession).filter(
        InterviewSession.id == ans_req.session_id,
        InterviewSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    answers = list(session.answers or [])
    # Update or append answer
    updated = False
    for a in answers:
        if a["question_id"] == ans_req.question_id:
            a["answer_text"] = ans_req.answer_text
            updated = True
            break
    if not updated:
        answers.append({
            "question_id": ans_req.question_id,
            "answer_text": ans_req.answer_text
        })

    session.answers = answers
    db.commit()
    return {"message": "Answer recorded", "recorded_count": len(answers)}

@router.post("/finish", response_model=InterviewFinishResponse)
async def finish_and_grade_interview(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    res = await interview_coach_agent.evaluate_answers(db, session.id, session.answers or [])
    return res

@router.get("/history", response_model=list[InterviewSessionOut])
def get_interview_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).order_by(InterviewSession.created_at.desc()).all()

    return [
        InterviewSessionOut(
            id=s.id,
            role=s.role,
            difficulty=s.difficulty,
            overall_score=s.overall_score or 0.0,
            created_at=s.created_at.strftime("%d %b %Y"),
            strengths=s.strengths or [],
            weak_skills=s.weak_skills or []
        )
        for s in sessions
    ]

