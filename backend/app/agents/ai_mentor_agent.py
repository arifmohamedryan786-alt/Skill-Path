from typing import Any, AsyncGenerator
from sqlalchemy.orm import Session
from backend.app.models import (
    User, Profile, ChatMessage, Career, Skill, Resource,
    RoadmapStage, RoadmapItem, AgentLog, AssessmentResult
)
from backend.app.models.practice import PracticeQuestion, PracticeProgress
from backend.app.agents.career_matcher_agent import career_matcher_agent
from backend.app.agents.simulation_agent import simulation_agent
from backend.app.agents.llm_client import llm_client, sanitize_user_input, AIBusyException

class AIMentorAgent:
    """
    Personalized AI Career Mentor:
    - Injects rich learner context into every interaction
    - Warm, concise (<250 words), step-by-step guidance
    - Executes tools (get_roadmap, get_gaps, explain_skill, etc.)
    - Provides interactive prompt chips
    - Proactive nudges and encouragement
    """

    DEFAULT_CHIPS = [
        "Where should I start this week?",
        "How is my coding practice going?",
        "When will I be job-ready?",
        "Recommend practice problems"
    ]

    def build_learner_context(self, db: Session, user_id: int) -> dict[str, Any]:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        career_goal = profile.career_goal if profile and profile.career_goal else "Not selected yet"

        career = db.query(Career).filter(Career.name.ilike(f"%{career_goal}%")).first()
        match_info = career_matcher_agent.calculate_match(db, user_id, career.id) if career else {}
        forecast_info = simulation_agent.calculate_forecast(db, user_id)

        recent_logs = db.query(AgentLog).filter(AgentLog.user_id == user_id).order_by(AgentLog.created_at.desc()).limit(3).all()
        recent_tests = db.query(AssessmentResult).filter(AssessmentResult.user_id == user_id).order_by(AssessmentResult.created_at.desc()).limit(2).all()

        # Practice Question statistics for context-aware guidance
        user_practice = db.query(PracticeProgress).filter(PracticeProgress.user_id == user_id).all()
        practice_completed = sum(1 for p in user_practice if p.status == "completed")
        practice_attempted = sum(1 for p in user_practice if p.status == "attempted")

        # Category-level breakdown
        cat_counts = {}
        for p in user_practice:
            if p.question:
                cat = p.question.category
                cat_counts[cat] = cat_counts.get(cat, {"completed": 0, "attempted": 0})
                if p.status == "completed":
                    cat_counts[cat]["completed"] += 1
                elif p.status == "attempted":
                    cat_counts[cat]["attempted"] += 1

        dsa_comp = cat_counts.get("DSA", {}).get("completed", 0)
        dsa_att = cat_counts.get("DSA", {}).get("attempted", 0)
        py_comp = cat_counts.get("Python", {}).get("completed", 0)

        practice_guidance = ""
        if dsa_att > 0 and dsa_comp < 3:
            practice_guidance = "You have attempted several DSA questions but have not completed the intermediate problems yet. I recommend revisiting arrays and searching algorithms before moving to advanced topics."
        elif py_comp >= 3:
            practice_guidance = f"You are performing well with {py_comp} Python questions completed! Consider tackling intermediate and advanced problem-solving questions."
        elif practice_completed == 0:
            practice_guidance = "You haven't completed any practice questions yet. Hands-on coding in C Programming or Python is the quickest way to build real confidence."
        else:
            practice_guidance = f"You have completed {practice_completed} questions so far. Consistent daily coding will accelerate your job-readiness date."

        return {
            "name": profile.full_name if profile else "Student",
            "education": f"{profile.education} in {profile.branch} (Year {profile.year})" if profile else "Student",
            "career_goal": career_goal,
            "match_pct": match_info.get("match_pct", 0.0),
            "readiness_label": match_info.get("readiness_label", "Beginning Explorer"),
            "gaps_count": match_info.get("gaps_count", 0),
            "weekly_hours": profile.weekly_hours if profile else 8.0,
            "pace_factor": profile.learner_pace_factor if profile else 1.0,
            "realistic_job_ready_date": forecast_info.get("realistic_date", "TBD"),
            "recent_actions": [f"{l.agent_name}: {l.action}" for l in recent_logs],
            "recent_scores": [f"Score: {t.score_pct}%" for t in recent_tests],
            "practice_completed": practice_completed,
            "practice_attempted": practice_attempted,
            "practice_guidance": practice_guidance,
            "cat_counts": cat_counts
        }

    async def generate_response(
        self,
        db: Session,
        user_id: int,
        user_message: str
    ) -> dict[str, Any]:
        clean_msg = sanitize_user_input(user_message)
        context = self.build_learner_context(db, user_id)

        # 1. Tool execution check
        lower = clean_msg.lower()
        tool_executed = None
        tool_data = None
        reply_text = ""
        suggested_chips = self.DEFAULT_CHIPS

        # Tool 1: Where should I start / roadmap
        if any(kw in lower for kw in ["start this week", "first week", "where should i start"]):
            tool_executed = "get_roadmap"
            reply_text = (
                f"Hello {context['name']}! Based on your target of {context['career_goal']}, here is your exact focus for this week:\n\n"
                f"1. **Primary Focus:** Start with foundational syntax in Python (30-45 mins/day).\n"
                f"2. **Hands-on Task:** Write a small script that creates a dictionary of your favorite books or movies.\n"
                f"3. **Checkpoint:** Take the Python Basics checkpoint quiz by Saturday to verify your retention.\n\n"
                f"Would you like me to open your personalized Day-by-Day schedule?"
            )
            suggested_chips = ["When will I be job-ready?", "Explain Python Basics", "Take checkpoint quiz"]

        # Tool 2: When will I be job-ready
        elif any(kw in lower for kw in ["job-ready", "when will i finish", "how long"]):
            tool_executed = "run_scenario"
            reply_text = (
                f"Great question! At your current study pace of **{context['weekly_hours']:.0f} hours per week**, "
                f"you are projected to become job-ready by **{context['realistic_job_ready_date']}**.\n\n"
                f"• **Current Match:** {context['match_pct']}%\n"
                f"• **Remaining Gap Skills:** {context['gaps_count']}\n\n"
                f"Want to finish sooner? If you increase your weekly study time to 12 hours/week in the Flight Simulator, you can reach job readiness nearly 4 weeks earlier!"
            )
            suggested_chips = ["Try 12 hours in simulator", "What skills are missing?", "Where should I start this week?"]

        # Tool 3: Career discovery help
        elif any(kw in lower for kw in ["don't know", "choose", "what career", "no idea"]):
            tool_executed = "get_discovery"
            reply_text = (
                f"That is completely normal, {context['name']}! Over 70% of students join SkillPath without knowing their exact career direction.\n\n"
                f"Because you are studying **{context['education']}**, roles like **AI/ML Engineer**, **Data Analyst**, and **Full Stack Developer** are natural fits.\n\n"
                f"The best way to know is to take our 15-question Career Discovery Assessment or try a 1-hour mini project. Shall we start discovery now?"
            )
            suggested_chips = ["Start Discovery Assessment", "Explore Data Analyst", "Explore Full Stack Developer"]

        # Tool 4: Explain a skill
        elif "explain" in lower:
            tool_executed = "explain_skill"
            # Extract potential skill
            skill = db.query(Skill).filter(Skill.slug == "python-basics").first()
            reply_text = (
                f"**Python** is a friendly programming language that reads almost like plain English.\n\n"
                f"Instead of dealing with confusing punctuation and memory pointers, Python lets you tell the computer what to do using clear indentation. "
                f"Almost all AI and machine learning tools (like PyTorch and Scikit-Learn) are built in Python.\n\n"
                f"Would you like to see the 'How to learn this' card for Python?"
            )
            suggested_chips = ["Show How to Learn card", "Give me a practice exercise", "Where should I start this week?"]

        # Tool 5: 12-month plan
        elif "12-month" in lower or "plan" in lower:
            tool_executed = "get_guide"
            reply_text = (
                f"Here is your 12-month trajectory to land a role as {context['career_goal']}:\n\n"
                f"• **Months 1-3:** Master programming foundations and Git version control.\n"
                f"• **Months 4-6:** Build core frameworks (Scikit-Learn, Pandas) and 2 portfolio projects.\n"
                f"• **Months 7-9:** Apply for summer internships and build an end-to-end Capstone project.\n"
                f"• **Months 10-12:** Practice mock interviews with our coach and apply to full-time roles.\n\n"
                f"You can view and export your complete Career Guide PDF anytime from the Career Guide page."
            )
            suggested_chips = ["Export Career Guide PDF", "Where should I start this week?", "When will I be job-ready?"]

        # Tool 6: Practice Questions & Coding Problem guidance
        elif any(kw in lower for kw in ["practice", "coding", "dsa", "problem", "exercise"]):
            tool_executed = "get_practice_guidance"
            completed = context["practice_completed"]
            attempted = context["practice_attempted"]
            guidance = context["practice_guidance"]
            reply_text = (
                f"Here is your real-time programming practice evaluation, **{context['name']}**:\n\n"
                f"• **Questions Completed:** {completed} / 50\n"
                f"• **Questions in Progress:** {attempted}\n\n"
                f"💡 **Mentor Analysis:**\n{guidance}\n\n"
                f"Hands-on coding strengthens retention by over 70% compared to just watching tutorials. "
                f"Shall we jump into the Practice Questions workspace?"
            )
            suggested_chips = ["Open Python Practice", "Open DSA Practice", "Where should I start this week?"]

        ai_busy = False
        if not tool_executed and not reply_text:
            # General Question: If LLM is available, use it with warm mentor persona
            if llm_client.is_available:
                system_prompt = (
                    f"You are the warm, encouraging AI Career Mentor for SkillPath. "
                    f"Student: {context['name']}, studying {context['education']}. "
                    f"Career Goal: {context['career_goal']} ({context['match_pct']}% match). "
                    f"Practice Questions Solved: {context['practice_completed']} completed, {context['practice_attempted']} attempted. "
                    f"Practice Assessment: {context['practice_guidance']} "
                    f"Job-ready forecast: {context['realistic_job_ready_date']}. "
                    f"Guidelines: Under 200 words, simple grade-8 language, step by step, "
                    f"ends with exactly ONE clear next action question. Never invent fake links or guarantee job placement."
                )
                try:
                    llm_ans = await llm_client.json(
                        prompt=clean_msg,
                        system_prompt=system_prompt,
                        user_id=user_id
                    )
                    if llm_ans and "reply" in llm_ans:
                        reply_text = llm_ans["reply"]
                    else:
                        reply_text = (
                            f"I'm here to support your career journey, {context['name']}! "
                            f"Whether you need help understanding a technical concept, preparing for an upcoming interview, "
                            f"or figuring out which skill to tackle today, just ask. What would you like to explore next?"
                        )
                except AIBusyException:
                    ai_busy = True
                    reply_text = (
                        f"⚠️ AI is busy, try again shortly. In the meantime, I'm using our offline knowledge base to guide you:\n\n"
                        f"For your target of {context['career_goal']}, your next milestone is advancing your core skills. "
                        f"What topic would you like to practice today?"
                    )
            else:
                reply_text = (
                    f"I'm right here with you, {context['name']}! As your SkillPath AI Mentor, "
                    f"I can help you explore suitable careers, break down complex topics into plain English, "
                    f"or optimize your study calendar so you become job-ready on time.\n\n"
                    f"What is on your mind today?"
                )

        # Save messages to database for per-user session memory
        user_chat = ChatMessage(user_id=user_id, role="user", content=clean_msg)
        asst_chat = ChatMessage(
            user_id=user_id,
            role="assistant",
            content=reply_text,
            metadata_json={"tool_executed": tool_executed, "suggested_chips": suggested_chips, "ai_busy": ai_busy}
        )
        db.add_all([user_chat, asst_chat])
        db.commit()

        return {
            "role": "assistant",
            "content": reply_text,
            "suggested_chips": suggested_chips,
            "tool_executed": tool_executed,
            "tool_data": tool_data,
            "ai_busy": ai_busy
        }

ai_mentor_agent = AIMentorAgent()

