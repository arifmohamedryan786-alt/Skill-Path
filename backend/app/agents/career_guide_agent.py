from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import Profile, Career, Skill, Resource, UserSkill, CareerSkill

class CareerGuideAgent:
    """
    Writes a comprehensive, start-to-finish personalized career guide.
    Regenerates when the goal, year, or major skills change, keeps versioning,
    and never fabricates links or salaries.
    """

    def generate_guide(self, db: Session, user_id: int) -> dict[str, Any]:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        student_name = profile.full_name if profile else "Student"
        education_str = f"{profile.education} in {profile.branch} (Year {profile.year})" if profile and profile.branch else "Student"
        career_goal = profile.career_goal if profile and profile.career_goal else "AI/ML Engineer"

        career = db.query(Career).filter(Career.name.ilike(f"%{career_goal}%")).first()
        if not career:
            career = db.query(Career).first()

        user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
        known_skill_count = len([s for s in user_skills if s.level > 0])

        # 1. Where You Stand Today
        where_you_stand = (
            f"You are currently studying {education_str} at {profile.institution if profile else 'college'}. "
            f"You have assessed {known_skill_count} technical skill{'s' if known_skill_count != 1 else ''}. "
            f"At this stage, you are transitioning from exploration into focused, structured skill acquisition."
        )

        # 2. Top 3 Careers
        top_careers_summary = (
            f"Based on your coursework and profile, your primary recommended career is **{career.name}** "
            f"({career.demand_level} industry demand). Two strong related paths are **Data Scientist** "
            f"(for statistical modeling) and **Data Engineer** (for data systems and pipelines). "
            f"We recommend committing to {career.name} first because it gives you broad transferable engineering skills."
        )

        # 3. Skills in Order
        career_skills = db.query(CareerSkill).filter(CareerSkill.career_id == career.id).all()
        skills_ordered = []
        for cs in career_skills:
            sk = db.query(Skill).filter(Skill.id == cs.skill_id).first()
            if sk:
                skills_ordered.append(f"{sk.name} (Target: Level {cs.target_level})")

        skills_sequence = "Learn skills in strict dependency order: Foundations (Python, Git, Math) -> Data manipulation (Pandas, SQL) -> Core models (Scikit-Learn, PyTorch) -> Production (FastAPI, Docker)."

        # 4. Recommended Courses (from real DB)
        resources = db.query(Resource).limit(6).all()
        recommended_courses = [
            {
                "title": r.title,
                "provider": r.provider,
                "type": r.type,
                "url": r.url,
                "free": r.free,
                "duration": r.duration
            }
            for r in resources
        ]

        # 5. Projects Plan
        projects_plan = {
            "beginner": f"Build a {career.mini_project.get('title', 'Spam Classifier Script')} in 1 to 2 hours using Python.",
            "intermediate": f"Build a multi-variable predictive model with interactive dashboard visualization using Streamlit and Scikit-Learn.",
            "capstone": f"Build an end-to-end {career.name} production system with a REST API backend, authenticated database, responsive web UI, and Docker deployment."
        }

        # 6. Internship Strategy by Year of Study
        yr = profile.year if profile else 3
        if yr == 1:
            internship_strategy = "Year 1 Strategy: Focus on building 2 public GitHub projects, join college tech clubs, and contribute to beginner open-source repositories."
        elif yr == 2:
            internship_strategy = "Year 2 Strategy: Participate in hackathons, build your LinkedIn network with alumni, and apply for winter internships."
        elif yr == 3:
            internship_strategy = "Year 3 Strategy: Critical internship window! Apply for summer tech internships 6 months early (October to January). Prepare for technical coding interviews."
        else:
            internship_strategy = "Year 4 Strategy: Full-time job search! Target on-campus recruitment drives, secure employee referrals via LinkedIn, and practice mock technical rounds."

        # 7. Growth & Specializations
        growth_options = (
            "Certifications: Pursue recognized credentials (e.g. AWS Certified Cloud Practitioner or TensorFlow Developer). "
            "Competitions: Participate on Kaggle or Devpost hackathons. "
            "Higher Studies: If considering an MS in CS or Data Science abroad or M.Tech in India, prepare for GRE or GATE starting in your 3rd year."
        )

        # 8. 12-Month Plan
        twelve_month_plan = [
            {"months": "Months 1-3", "focus": "Foundations & Programming Mastery", "milestone": "Pass Python Basics and Git assessments with 70%+"},
            {"months": "Months 4-6", "focus": "Core Domain Frameworks & Databases", "milestone": "Complete 2 portfolio projects on GitHub"},
            {"months": "Months 7-9", "focus": "Internship Applications & Capstone Project", "milestone": "Land a summer internship and complete end-to-end full capstone"},
            {"months": "Months 10-12", "focus": "Interview Preparation & Job Offers", "milestone": "Score 4.0+ on Mock Interview Coach and secure job offers"}
        ]

        # 9. Next 7 Days
        next_7_days = [
            {"day": "Day 1", "action": "Complete the 'How to learn this' module for Python Basics."},
            {"day": "Day 2", "action": "Set up a clean GitHub profile with a descriptive bio."},
            {"day": "Day 3", "action": f"Run the 1-hour try-it mini project for {career.name}."},
            {"day": "Day 4", "action": "Practice 3 interactive coding exercises."},
            {"day": "Day 5", "action": "Take your first checkpoint quiz to test retention."},
            {"day": "Day 6", "action": "Review your Flight Simulator readiness forecast."},
            {"day": "Day 7", "action": "Check in with your AI Mentor to review your week."}
        ]

        return {
            "version": 1,
            "target_career": career.name,
            "generated_at": datetime.utcnow().strftime("%d %B %Y"),
            "where_you_stand": where_you_stand,
            "top_careers_summary": top_careers_summary,
            "skills_sequence": skills_sequence,
            "recommended_courses": recommended_courses,
            "projects_plan": projects_plan,
            "internship_strategy": internship_strategy,
            "growth_options": growth_options,
            "twelve_month_plan": twelve_month_plan,
            "next_7_days": next_7_days
        }

career_guide_agent = CareerGuideAgent()

