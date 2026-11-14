from typing import Optional, Any
from pydantic import BaseModel

class InterviewQuestion(BaseModel):
    id: int
    topic: str
    question: str
    hint: Optional[str] = None

class InterviewStartRequest(BaseModel):
    role: Optional[str] = None
    difficulty: Optional[str] = "Junior" # "Intern", "Junior", "Mid-level"

class InterviewStartResponse(BaseModel):
    session_id: int
    role: str
    difficulty: str
    questions: list[InterviewQuestion]
    total_questions: int

class InterviewAnswerRequest(BaseModel):
    session_id: int
    question_id: int
    answer_text: str

class RubricBreakdown(BaseModel):
    correctness: float # 1-5
    depth: float       # 1-5
    clarity: float     # 1-5
    examples: float    # 1-5
    overall: float     # 1-5

class SampleAnswerItem(BaseModel):
    question_id: int
    question: str
    ideal_answer: str

class InterviewFinishResponse(BaseModel):
    session_id: int
    role: str
    difficulty: str
    rubric_scores: RubricBreakdown
    strengths: list[str]
    mistakes: list[str]
    sample_answers: list[SampleAnswerItem]
    practice_items: list[dict[str, str]]
    weak_skills: list[str]
    adaptation_note: str

class InterviewSessionOut(BaseModel):
    id: int
    role: str
    difficulty: str
    overall_score: float
    created_at: str
    strengths: list[str]
    weak_skills: list[str]

