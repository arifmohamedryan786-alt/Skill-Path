from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.practice import PracticeQuestion, PracticeProgress
from backend.app.models.user import User
from backend.app.models.agent_log import AgentLog
from backend.app.api.deps import get_current_user
from backend.app.agents.progress_evaluator_agent import progress_evaluator_agent

router = APIRouter(prefix="/practice", tags=["Practice Questions"])

# ==============================================================================
# Pydantic Schemas
# ==============================================================================

class CategoryInfo(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    icon: str
    total_questions: int
    completed_questions: int
    attempted_questions: int
    beginner_count: int
    intermediate_count: int
    advanced_count: int

class QuestionSummaryOut(BaseModel):
    id: int
    category: str
    category_slug: str
    title: str
    difficulty: str
    description: str
    order_index: int
    user_status: str              # "not_started", "attempted", "completed"
    has_saved_code: bool

class QuestionDetailOut(BaseModel):
    id: int
    category: str
    category_slug: str
    title: str
    difficulty: str
    description: str
    example_input: str
    example_output: str
    hint: str
    starter_code: str
    solution: str
    explanation: str
    approach: str
    time_complexity: str
    space_complexity: str
    order_index: int
    user_status: str              # "not_started", "attempted", "completed"
    user_solution_code: str
    completed_at: Optional[str] = None
    next_question_id: Optional[int] = None
    prev_question_id: Optional[int] = None

class ProgressUpdateRequest(BaseModel):
    status: Optional[str] = None   # "attempted", "completed"
    solution_code: Optional[str] = None

class PracticeStatsOut(BaseModel):
    total_completed: int
    total_attempted: int
    total_questions: int
    completion_pct: float
    current_streak: int
    by_category: dict
    by_difficulty: dict
    recent_activity: List[dict]

# ==============================================================================
# Static Category Definitions
# ==============================================================================

CATEGORIES_META = [
    {
        "id": "c-programming",
        "name": "C Programming",
        "slug": "c-programming",
        "description": "Practice fundamentals including variables, loops, functions, arrays and pointers.",
        "icon": "Terminal"
    },
    {
        "id": "python",
        "name": "Python",
        "slug": "python",
        "description": "Practice Python syntax, functions, lists, dictionaries and problem-solving.",
        "icon": "Code2"
    },
    {
        "id": "java",
        "name": "Java",
        "slug": "java",
        "description": "Practice object-oriented programming, classes, inheritance and core Java concepts.",
        "icon": "Coffee"
    },
    {
        "id": "data-structures",
        "name": "Data Structures",
        "slug": "data-structures",
        "description": "Practice arrays, linked lists, stacks, queues, trees and graphs.",
        "icon": "Network"
    },
    {
        "id": "dsa",
        "name": "DSA",
        "slug": "dsa",
        "description": "Practice algorithms including searching, sorting, recursion, dynamic programming and problem-solving.",
        "icon": "Cpu"
    }
]

# ==============================================================================
# API Routes
# ==============================================================================

@router.get("/categories", response_model=List[CategoryInfo])
def get_practice_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the 5 interactive practice categories with live question counts
    and learner progress meters.
    """
    # Fetch user's completed question IDs
    user_progress_list = db.query(PracticeProgress).filter(
        PracticeProgress.user_id == current_user.id
    ).all()

    completed_q_ids = {p.question_id for p in user_progress_list if p.status == "completed"}
    attempted_q_ids = {p.question_id for p in user_progress_list if p.status == "attempted"}

    categories_out = []
    for cat in CATEGORIES_META:
        questions = db.query(PracticeQuestion).filter(
            PracticeQuestion.category_slug == cat["slug"]
        ).all()

        total = len(questions)
        completed = sum(1 for q in questions if q.id in completed_q_ids)
        attempted = sum(1 for q in questions if q.id in attempted_q_ids)
        beg = sum(1 for q in questions if q.difficulty == "Beginner")
        inter = sum(1 for q in questions if q.difficulty == "Intermediate")
        adv = sum(1 for q in questions if q.difficulty == "Advanced")

        categories_out.append(CategoryInfo(
            id=cat["id"],
            name=cat["name"],
            slug=cat["slug"],
            description=cat["description"],
            icon=cat["icon"],
            total_questions=total,
            completed_questions=completed,
            attempted_questions=attempted,
            beginner_count=beg,
            intermediate_count=inter,
            advanced_count=adv
        ))

    return categories_out


@router.get("/questions", response_model=List[QuestionSummaryOut])
def get_practice_questions(
    category: Optional[str] = Query(None, description="Category slug or name"),
    difficulty: Optional[str] = Query(None, description="Beginner, Intermediate, Advanced"),
    status: Optional[str] = Query(None, description="all, completed, attempted, uncompleted"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns filtered practice questions with learner's current progress status.
    """
    query = db.query(PracticeQuestion)

    if category and category.lower() != "all":
        clean_cat = category.strip().lower()
        query = query.filter(
            (PracticeQuestion.category_slug == clean_cat) |
            (PracticeQuestion.category.ilike(f"%{category}%"))
        )

    if difficulty and difficulty.lower() != "all":
        query = query.filter(PracticeQuestion.difficulty.ilike(difficulty.strip()))

    questions = query.order_by(PracticeQuestion.order_index).all()

    # User progress map
    user_prog = {
        p.question_id: p
        for p in db.query(PracticeProgress).filter(PracticeProgress.user_id == current_user.id).all()
    }

    results = []
    for q in questions:
        prog = user_prog.get(q.id)
        user_status = prog.status if prog else "not_started"
        has_saved_code = bool(prog and prog.solution_code and prog.solution_code.strip())

        # Filter by completion status
        if status == "completed" and user_status != "completed":
            continue
        elif status == "attempted" and user_status != "attempted":
            continue
        elif status == "uncompleted" and user_status == "completed":
            continue

        results.append(QuestionSummaryOut(
            id=q.id,
            category=q.category,
            category_slug=q.category_slug,
            title=q.title,
            difficulty=q.difficulty,
            description=q.description,
            order_index=q.order_index,
            user_status=user_status,
            has_saved_code=has_saved_code
        ))

    return results


@router.get("/questions/{question_id}", response_model=QuestionDetailOut)
def get_question_detail(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns single question with full solution, hints, starter code,
    and user's saved workspace solution. Also provides prev/next IDs.
    """
    q = db.query(PracticeQuestion).filter(PracticeQuestion.id == question_id).first()
    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Practice question #{question_id} not found."
        )

    prog = db.query(PracticeProgress).filter(
        PracticeProgress.user_id == current_user.id,
        PracticeProgress.question_id == q.id
    ).first()

    # Find next and previous questions in the same category or overall
    prev_q = db.query(PracticeQuestion).filter(
        PracticeQuestion.category_slug == q.category_slug,
        PracticeQuestion.order_index < q.order_index
    ).order_by(PracticeQuestion.order_index.desc()).first()

    next_q = db.query(PracticeQuestion).filter(
        PracticeQuestion.category_slug == q.category_slug,
        PracticeQuestion.order_index > q.order_index
    ).order_by(PracticeQuestion.order_index.asc()).first()

    # If no next in same category, look globally
    if not next_q:
        next_q = db.query(PracticeQuestion).filter(PracticeQuestion.order_index > q.order_index).order_by(PracticeQuestion.order_index.asc()).first()
    if not prev_q:
        prev_q = db.query(PracticeQuestion).filter(PracticeQuestion.order_index < q.order_index).order_by(PracticeQuestion.order_index.desc()).first()

    return QuestionDetailOut(
        id=q.id,
        category=q.category,
        category_slug=q.category_slug,
        title=q.title,
        difficulty=q.difficulty,
        description=q.description,
        example_input=q.example_input,
        example_output=q.example_output,
        hint=q.hint,
        starter_code=q.starter_code,
        solution=q.solution,
        explanation=q.explanation,
        approach=q.approach,
        time_complexity=q.time_complexity,
        space_complexity=q.space_complexity,
        order_index=q.order_index,
        user_status=prog.status if prog else "not_started",
        user_solution_code=prog.solution_code if prog and prog.solution_code else q.starter_code,
        completed_at=prog.completed_at.strftime("%b %d, %Y") if prog and prog.completed_at else None,
        next_question_id=next_q.id if next_q else None,
        prev_question_id=prev_q.id if prev_q else None
    )


@router.post("/questions/{question_id}/progress")
def update_question_progress(
    question_id: int,
    payload: ProgressUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Saves solution code and/or marks a practice problem as completed or attempted.
    """
    q = db.query(PracticeQuestion).filter(PracticeQuestion.id == question_id).first()
    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Practice question #{question_id} not found."
        )

    prog = db.query(PracticeProgress).filter(
        PracticeProgress.user_id == current_user.id,
        PracticeProgress.question_id == q.id
    ).first()

    now = datetime.utcnow()
    newly_completed = False

    if not prog:
        prog = PracticeProgress(
            user_id=current_user.id,
            question_id=q.id,
            status=payload.status or "attempted",
            solution_code=payload.solution_code or "",
            completed_at=now if payload.status == "completed" else None,
            updated_at=now
        )
        db.add(prog)
        if payload.status == "completed":
            newly_completed = True
    else:
        if payload.solution_code is not None:
            prog.solution_code = payload.solution_code
        if payload.status:
            if payload.status == "completed" and prog.status != "completed":
                prog.completed_at = now
                newly_completed = True
            prog.status = payload.status
        prog.updated_at = now

    db.commit()

    # Log milestone and recalculate learning velocity if completed
    if newly_completed:
        log = AgentLog(
            user_id=current_user.id,
            agent_name="Progress Evaluator Agent",
            action="Practice Problem Completed",
            reason=f"Successfully solved {q.category} problem '{q.title}' ({q.difficulty}).",
            details={
                "question_id": q.id,
                "category": q.category,
                "difficulty": q.difficulty,
                "title": q.title
            }
        )
        db.add(log)
        db.commit()

        # Update velocity factor
        progress_evaluator_agent.evaluate_pace_factor(db, current_user.id)

    return {
        "status": "success",
        "question_id": q.id,
        "user_status": prog.status,
        "completed_at": prog.completed_at.isoformat() if prog.completed_at else None,
        "message": f"Problem '{q.title}' marked as {prog.status}."
    }


@router.get("/stats", response_model=PracticeStatsOut)
def get_practice_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns user practice statistics including category breakdown,
    difficulty breakdown, completion percentage, and streak.
    """
    all_questions = db.query(PracticeQuestion).all()
    total_q = len(all_questions)

    user_progress = db.query(PracticeProgress).filter(
        PracticeProgress.user_id == current_user.id
    ).all()

    completed_ids = {p.question_id for p in user_progress if p.status == "completed"}
    attempted_ids = {p.question_id for p in user_progress if p.status == "attempted"}

    # Category breakdown
    by_category = {}
    for cat in CATEGORIES_META:
        cat_qs = [q for q in all_questions if q.category_slug == cat["slug"]]
        comp = sum(1 for q in cat_qs if q.id in completed_ids)
        by_category[cat["name"]] = {
            "slug": cat["slug"],
            "completed": comp,
            "total": len(cat_qs),
            "pct": round((comp / len(cat_qs) * 100), 1) if cat_qs else 0.0
        }

    # Difficulty breakdown
    by_difficulty = {}
    for diff in ["Beginner", "Intermediate", "Advanced"]:
        diff_qs = [q for q in all_questions if q.difficulty == diff]
        comp = sum(1 for q in diff_qs if q.id in completed_ids)
        by_difficulty[diff] = {
            "completed": comp,
            "total": len(diff_qs),
            "pct": round((comp / len(diff_qs) * 100), 1) if diff_qs else 0.0
        }

    # Recent activity
    recent = []
    completed_progress = sorted(
        [p for p in user_progress if p.completed_at is not None],
        key=lambda x: x.completed_at,
        reverse=True
    )[:5]

    for cp in completed_progress:
        q_obj = next((q for q in all_questions if q.id == cp.question_id), None)
        if q_obj:
            recent.append({
                "question_id": q_obj.id,
                "title": q_obj.title,
                "category": q_obj.category,
                "difficulty": q_obj.difficulty,
                "completed_at": cp.completed_at.strftime("%b %d, %H:%M")
            })

    total_completed = len(completed_ids)
    pct = round((total_completed / max(total_q, 1)) * 100, 1)

    # Dynamic practice streak based on completed count
    streak = 1 if total_completed > 0 else 0
    if total_completed >= 5:
        streak = 3
    if total_completed >= 10:
        streak = 7

    return PracticeStatsOut(
        total_completed=total_completed,
        total_attempted=len(attempted_ids),
        total_questions=total_q,
        completion_pct=pct,
        current_streak=streak,
        by_category=by_category,
        by_difficulty=by_difficulty,
        recent_activity=recent
    )

