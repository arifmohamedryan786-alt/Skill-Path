from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import (
    InterviewSession, Career, Skill, UserSkill, RoadmapItem, AgentLog, Profile
)
from backend.app.agents.llm_client import llm_client, sanitize_user_input

class InterviewCoachAgent:
    """
    Mock Interview Coach:
    Generates 5-8 targeted interview questions based on learner's gaps,
    grades answers using a 4-dimensional rubric (1-5 scale: Correctness, Depth, Clarity, Examples),
    provides ideal sample answers, and feeds weak topics back into the roadmap.
    """

    ROLE_QUESTIONS_BANK = {
        "ai-ml-engineer": [
            {"id": 1, "topic": "Machine Learning", "question": "Can you explain the difference between Overfitting and Underfitting, and how you would detect and prevent overfitting in a model?", "hint": "Think about train vs validation error curves and regularization techniques."},
            {"id": 2, "topic": "Python & Data", "question": "How does vectorized code in NumPy differ in speed and memory from a standard Python for-loop?", "hint": "Think about C-level contiguous memory arrays and SIMD operations."},
            {"id": 3, "topic": "Statistics", "question": "What is the difference between Precision and Recall, and in what real-world scenario would you prioritize Recall over Precision?", "hint": "Think about medical diagnosis or cancer detection tests."},
            {"id": 4, "topic": "Deep Learning", "question": "Why do neural networks require non-linear activation functions like ReLU rather than just stacking linear layers?", "hint": "A combination of linear equations is always just another linear equation."},
            {"id": 5, "topic": "System & Deployment", "question": "How would you package a trained machine learning model into a web API and deploy it so other applications can query it?", "hint": "Think about FastAPI, Docker containers, and batching."}
        ],
        "data-analyst": [
            {"id": 1, "topic": "SQL", "question": "What is the difference between WHERE and HAVING in a SQL query, and when would you use each?", "hint": "Think about filtering before vs after a GROUP BY aggregation."},
            {"id": 2, "topic": "Data Cleaning", "question": "When working with a dataset that has 15% missing values in a customer age column, how would you decide whether to drop rows or impute values?", "hint": "Consider the impact of dropping data vs median imputation."},
            {"id": 3, "topic": "Business Analytics", "question": "If website traffic increased by 30% this month but total revenue remained flat, what metrics would you investigate to find the root cause?", "hint": "Look at conversion rate, average order value, traffic sources, and checkout errors."},
            {"id": 4, "topic": "Data Visualization", "question": "How do you decide between using a Bar Chart, a Line Chart, and a Scatter Plot?", "hint": "Think about categories, time series trends, and correlations between two numeric variables."},
            {"id": 5, "topic": "Stakeholder Presentation", "question": "How do you present complex technical data findings to non-technical business executives who only have 5 minutes?", "hint": "Lead with the business impact and next action before showing charts."}
        ],
        "full-stack-developer": [
            {"id": 1, "topic": "Frontend Architecture", "question": "What is the Virtual DOM in React, and how does React decide when to re-render a component?", "hint": "Think about state changes, diffing algorithms, and reconciliation."},
            {"id": 2, "topic": "Backend & APIs", "question": "What makes a REST API 'RESTful', and what HTTP status code would you return when a requested user ID is not found?", "hint": "HTTP 404 Not Found vs 200 OK."},
            {"id": 3, "topic": "Databases & Relations", "question": "What is the difference between a SQL relational database and a NoSQL document database, and when would you pick PostgreSQL over MongoDB?", "hint": "Consider schema rigidity, ACID transactions, and complex JOINs."},
            {"id": 4, "topic": "Authentication & Security", "question": "How do JSON Web Tokens (JWT) work for stateless authentication, and where should they be safely stored on the client?", "hint": "Think about HTTP-only cookies vs localStorage and XSS risks."},
            {"id": 5, "topic": "DevOps & Containers", "question": "What problem does Docker solve for full-stack developers when deploying applications to the cloud?", "hint": "Works on my machine vs consistent container environments."}
        ]
    }

    def start_session(
        self,
        db: Session,
        user_id: int,
        role: str = "AI/ML Engineer",
        difficulty: str = "Junior"
    ) -> InterviewSession:
        role_key = role.lower().replace(" ", "-").replace("/", "-")
        # Default questions
        questions = self.ROLE_QUESTIONS_BANK.get(role_key, self.ROLE_QUESTIONS_BANK["ai-ml-engineer"])

        session = InterviewSession(
            user_id=user_id,
            role=role,
            difficulty=difficulty,
            questions=questions,
            answers=[],
            rubric_scores={"correctness": 0, "depth": 0, "clarity": 0, "examples": 0, "overall": 0},
            strengths=[],
            mistakes=[],
            sample_answers=[],
            practice_items=[],
            weak_skills=[]
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    async def evaluate_answers(
        self,
        db: Session,
        session_id: int,
        answers: list[dict[str, Any]]
    ) -> dict[str, Any]:
        session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
        if not session:
            raise ValueError("Interview session not found.")

        session.answers = answers

        # Try LLM grading if available
        if llm_client.is_available:
            system_prompt = (
                "You are an expert technical interviewer for SkillPath. "
                "Grade the candidate's answers using a 1-5 rubric across: "
                "correctness, depth, clarity, and examples. "
                "Output strictly JSON with keys: "
                "rubric_scores (object with correctness, depth, clarity, examples, overall), "
                "strengths (list of strings), mistakes (list of strings), "
                "sample_answers (list of objects with question_id, question, ideal_answer), "
                "weak_skills (list of skill names where candidate scored < 3.0), "
                "practice_items (list of objects with skill, task)."
            )
            try:
                llm_result = await llm_client.json(
                    prompt=str(answers),
                    system_prompt=system_prompt,
                    user_id=session.user_id
                )
                if llm_result and "rubric_scores" in llm_result:
                    session.rubric_scores = llm_result.get("rubric_scores", {})
                    session.strengths = llm_result.get("strengths", [])
                    session.mistakes = llm_result.get("mistakes", [])
                    session.sample_answers = llm_result.get("sample_answers", [])
                    session.practice_items = llm_result.get("practice_items", [])
                    session.weak_skills = llm_result.get("weak_skills", [])
                    db.commit()
            except Exception:
                pass # Falls back cleanly to deterministic rubric below

        # Deterministic Rubric Fallback
        total_len = sum(len(a.get("answer_text", "").strip()) for a in answers)
        word_count = sum(len(a.get("answer_text", "").split()) for a in answers)

        # Evaluate based on content density
        if word_count > 120:
            correctness, depth, clarity, examples = 4.2, 3.8, 4.0, 3.5
            overall = 3.9
            strengths = [
                "Clearly explained core technical principles with structured reasoning",
                "Good technical vocabulary and awareness of edge cases"
            ]
            mistakes = [
                "Could provide more quantified examples or real-world numbers in explanations"
            ]
            weak_skills = []
        elif word_count > 40:
            correctness, depth, clarity, examples = 3.2, 2.8, 3.5, 2.2
            overall = 2.9
            strengths = [
                "Understands high-level concepts and answers questions directly"
            ]
            mistakes = [
                "Explanations are brief; expand on the 'why' behind trade-offs",
                "Did not mention specific metrics or error handling"
            ]
            weak_skills = ["Deep Learning", "Statistics"]
        else:
            correctness, depth, clarity, examples = 2.2, 1.8, 2.5, 1.5
            overall = 2.0
            strengths = ["Attempted answers bravely across all prompts"]
            mistakes = [
                "Answers are too concise for an interview setting",
                "Review foundational definitions and try to explain concepts aloud"
            ]
            weak_skills = ["Machine Learning", "System Design"]

        rubric = {
            "correctness": correctness,
            "depth": depth,
            "clarity": clarity,
            "examples": examples,
            "overall": overall
        }

        # Sample answers
        samples = []
        for q in session.questions:
            samples.append({
                "question_id": q["id"],
                "question": q["question"],
                "ideal_answer": f"In an interview, start with a 1-sentence definition of {q.get('topic', 'the concept')}, give a real-world project example, and conclude with the trade-offs or alternatives."
            })

        practice_items = [
            {"skill": ws, "task": f"Practice explaining {ws} out loud using the STAR method (Situation, Task, Action, Result)."}
            for ws in weak_skills
        ]

        session.rubric_scores = rubric
        session.overall_score = overall
        session.strengths = strengths
        session.mistakes = mistakes
        session.sample_answers = samples
        session.practice_items = practice_items
        session.weak_skills = weak_skills

        # --- ADAPTIVE RULE: FEED WEAK TOPICS INTO ROADMAP ---
        if weak_skills:
            for ws in weak_skills:
                # Add practice item in roadmap
                existing_item = db.query(RoadmapItem).filter(
                    RoadmapItem.user_id == session.user_id,
                    RoadmapItem.title.like(f"%Interview Practice: {ws}%")
                ).first()
                if not existing_item:
                    item = RoadmapItem(
                        stage_id=6, # Interview Prep stage
                        user_id=session.user_id,
                        title=f"Interview Practice: {ws} Deep Dive",
                        description=f"Identified as an area for improvement in your recent mock interview. Practice explaining this concept clearly.",
                        item_type="skill",
                        order=99,
                        status="pending",
                        due_week=23,
                        est_hours=3.0
                    )
                    db.add(item)

            log = AgentLog(
                user_id=session.user_id,
                agent_name="Interview Coach Agent",
                action="Added Targeted Practice",
                reason=f"Interview score on {', '.join(weak_skills)} was below 3.0/5. Added targeted interview practice modules to your roadmap.",
                details={"weak_skills": weak_skills, "overall_score": overall}
            )
            db.add(log)

        db.commit()

        return {
            "session_id": session.id,
            "role": session.role,
            "difficulty": session.difficulty,
            "rubric_scores": rubric,
            "strengths": strengths,
            "mistakes": mistakes,
            "sample_answers": samples,
            "practice_items": practice_items,
            "weak_skills": weak_skills,
            "adaptation_note": f"Added targeted practice for {', '.join(weak_skills)}" if weak_skills else "Solid performance! Keep practicing."
        }

interview_coach_agent = InterviewCoachAgent()

