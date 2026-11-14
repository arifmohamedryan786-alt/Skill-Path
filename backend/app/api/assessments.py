from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.assessment import Assessment, AssessmentResult
from backend.app.models.skill import Skill
from backend.app.models.user import User
from backend.app.schemas.assessment import AssessmentOut, AssessmentSubmitRequest, AssessmentResultOut, MCQQuestion, PracticalTask
from backend.app.api.deps import get_current_user
from backend.app.agents.assessment_agent import assessment_agent
from backend.app.seed.seed_assessments import ASSESSMENTS_DATA

router = APIRouter(prefix="/assessments", tags=["Assessments & Verification"])

@router.get("/generate", response_model=AssessmentOut)
def generate_assessment(
    skill_slug: str = "python-basics",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(Skill.slug == skill_slug).first()
    if not skill:
        skill = db.query(Skill).first()

    assessment = db.query(Assessment).filter(Assessment.skill_id == skill.id).first()
    if not assessment:
        # Dynamically seed assessment if not present in DB
        a_data = ASSESSMENTS_DATA.get(skill.slug)
        if not a_data:
            # Generate sensible default MCQs
            a_data = {
                "title": f"{skill.name} Core Proficiency Checkpoint",
                "description": f"Validates your practical grasp of {skill.name}.",
                "target_level": 2,
                "questions": [
                    {"id": 1, "question": f"What is the primary role of {skill.name} in modern applications?", "options": ["Automating tasks and managing data", "Formatting physical paper", "Designing graphics", "Replacing operating systems"], "correct_index": 0, "explanation": "It provides programmatic control and automation."},
                    {"id": 2, "question": "Which principle should you follow when structuring your solutions?", "options": ["Single Responsibility Principle", "Write everything in one file", "Avoid comments", "Ignore edge cases"], "correct_index": 0, "explanation": "Keep modules focused on one clear task."},
                    {"id": 3, "question": "What is the recommended approach to handling runtime errors?", "options": ["Graceful try-except blocks", "Ignoring errors", "Restarting computer", "Hardcoding inputs"], "correct_index": 0, "explanation": "Catch and log exceptions safely."},
                    {"id": 4, "question": "How do you verify your code behaves correctly before deploying?", "options": ["Write automated unit tests", "Trust it works", "Delete older code", "Skip validation"], "correct_index": 0, "explanation": "Automated testing catches bugs early."},
                    {"id": 5, "question": "What tool enables safe version control and collaboration?", "options": ["Git & GitHub", "Email attachments", "Notepad", "USB Drives"], "correct_index": 0, "explanation": "Git tracks changes and supports safe branching."}
                ],
                "practical_task": {
                    "prompt": f"Write a function or query demonstrating {skill.name} fundamentals.",
                    "hint": "Focus on clean syntax and handling empty inputs.",
                    "evaluation_criteria": "Valid syntax with correct output.",
                    "starter_code": "# Write solution below\n"
                }
            }
        assessment = Assessment(
            skill_id=skill.id,
            title=a_data["title"],
            description=a_data["description"],
            target_level=a_data["target_level"],
            questions=a_data["questions"],
            practical_task=a_data["practical_task"]
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)

    # Convert questions to safe MCQQuestion without revealing correct_index to client
    safe_mcqs = [
        MCQQuestion(
            id=q["id"],
            question=q["question"],
            options=q["options"],
            explanation=None
        )
        for q in assessment.questions
    ]

    pt = assessment.practical_task or {}
    practical = PracticalTask(
        prompt=pt.get("prompt", "Write a small code solution."),
        hint=pt.get("hint", ""),
        evaluation_criteria=pt.get("evaluation_criteria", "Correct logic"),
        starter_code=pt.get("starter_code", "")
    )

    return AssessmentOut(
        id=assessment.id,
        skill_id=skill.id,
        skill_name=skill.name,
        title=assessment.title,
        description=assessment.description,
        target_level=assessment.target_level,
        questions=safe_mcqs,
        practical_task=practical
    )

@router.post("/submit", response_model=AssessmentResultOut)
def submit_assessment(
    sub_req: AssessmentSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    res = assessment_agent.grade_assessment(
        db=db,
        user_id=current_user.id,
        assessment_id=sub_req.assessment_id,
        mcq_answers=sub_req.mcq_answers,
        practical_submission=sub_req.practical_code or ""
    )
    return res

