from typing import Optional, Any
from pydantic import BaseModel

class MCQQuestion(BaseModel):
    id: int
    question: str
    options: list[str]
    # correct_index is hidden in client display
    explanation: Optional[str] = None

class PracticalTask(BaseModel):
    prompt: str
    hint: str
    evaluation_criteria: str
    starter_code: Optional[str] = None

class AssessmentOut(BaseModel):
    id: int
    skill_id: int
    skill_name: str
    title: str
    description: str
    target_level: int
    questions: list[MCQQuestion]
    practical_task: PracticalTask

class AssessmentSubmitRequest(BaseModel):
    assessment_id: int
    mcq_answers: dict[int, int] # {question_id: selected_index}
    practical_code: Optional[str] = ""

class AssessmentResultOut(BaseModel):
    result_id: int
    skill_id: int
    skill_name: str
    score_pct: float
    passed: bool
    status_label: str # "Verified Mastered", "Partial Progress", "Remedial Needed"
    correct_count: int
    total_mcqs: int
    feedback_summary: str
    remedial_topics: list[str]
    next_action: str
    updated_level: int
    verification_hash: Optional[str] = None

