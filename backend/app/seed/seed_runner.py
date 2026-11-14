import os
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.database import engine, SessionLocal, Base
from backend.app.models import (
    User, Profile, Career, Skill, CareerSkill, Resource,
    Glossary, Organization, Cohort, UserSkill, Assessment, SkillPassport
)
from backend.app.models.practice import PracticeQuestion, PracticeProgress
from backend.app.utils.security import get_password_hash
from backend.app.seed.seed_data import CAREERS_DATA
from backend.app.seed.seed_skills_resources import ALL_SKILLS_DATA, ALL_RESOURCES_DATA, CAREER_SKILLS_MAP
from backend.app.seed.seed_glossary import GLOSSARY_DATA
from backend.app.seed.seed_assessments import ASSESSMENTS_DATA
from backend.app.seed.seed_practice_questions import PRACTICE_QUESTIONS_DATA

def seed_practice_questions(db: Session):
    count = db.query(PracticeQuestion).count()
    if count == 0:
        print("💻 Seeding 50 Practice Questions across 5 Categories...")
        for q in PRACTICE_QUESTIONS_DATA:
            pq = PracticeQuestion(
                category=q["category"],
                category_slug=q["category_slug"],
                title=q["title"],
                difficulty=q["difficulty"],
                order_index=q["order_index"],
                description=q["description"],
                example_input=q.get("example_input", ""),
                example_output=q.get("example_output", ""),
                hint=q.get("hint", ""),
                starter_code=q.get("starter_code", ""),
                solution=q.get("solution", ""),
                explanation=q.get("explanation", ""),
                approach=q.get("approach", ""),
                time_complexity=q.get("time_complexity", "O(N)"),
                space_complexity=q.get("space_complexity", "O(1)")
            )
            db.add(pq)
        db.flush()

        # Seed sample progress for demo personas if users exist
        arif_user = db.query(User).filter(User.email == "arif@skillpath.dev").first()
        rohan_user = db.query(User).filter(User.email == "rohan@skillpath.dev").first()
        priya_user = db.query(User).filter(User.email == "priya@skillpath.dev").first()

        q_map = {q.order_index: q for q in db.query(PracticeQuestion).all()}

        if arif_user and 11 in q_map and 41 in q_map:
            db.add(PracticeProgress(
                user_id=arif_user.id,
                question_id=q_map[11].id,
                status="completed",
                solution_code="def reverse_string(s):\n    return s[::-1]",
                completed_at=datetime.utcnow()
            ))
            db.add(PracticeProgress(
                user_id=arif_user.id,
                question_id=q_map[41].id,
                status="completed",
                solution_code="def linear_search(arr, target):\n    for i, v in enumerate(arr):\n        if v == target: return i\n    return -1",
                completed_at=datetime.utcnow()
            ))
            db.add(PracticeProgress(
                user_id=arif_user.id,
                question_id=q_map[42].id,
                status="attempted",
                solution_code="def binary_search(nums, target):\n    # In progress...",
                completed_at=None
            ))

        if rohan_user and 11 in q_map and 12 in q_map and 13 in q_map and 15 in q_map:
            for q_idx in [11, 12, 13, 15]:
                db.add(PracticeProgress(
                    user_id=rohan_user.id,
                    question_id=q_map[q_idx].id,
                    status="completed",
                    solution_code="# Solved by Rohan",
                    completed_at=datetime.utcnow()
                ))

        if priya_user and 1 in q_map:
            db.add(PracticeProgress(
                user_id=priya_user.id,
                question_id=q_map[1].id,
                status="attempted",
                solution_code="# Learning C syntax...",
                completed_at=None
            ))

        db.commit()
        print("✅ 50 Practice Questions successfully seeded!")

def seed_database(target_engine=None, target_sessionmaker=None):
    use_engine = target_engine or engine
    use_sessionmaker = target_sessionmaker or SessionLocal
    print("🌱 Initializing SkillPath Database & Tables...")
    Base.metadata.create_all(bind=use_engine)
    db: Session = use_sessionmaker()

    try:
        # Check if already seeded
        if db.query(Career).count() > 0:
            print("Database already has records. Running refresh check...")
            seed_practice_questions(db)
            return

        # 1. Organizations & Cohorts
        print("🏛️ Creating Universities & Cohorts...")
        org = Organization(name="National Institute of Technology", slug="nit-edu", type="university")
        db.add(org)
        db.flush()

        cohort1 = Cohort(org_id=org.id, name="B.Tech AI & Data Science - 2026 Batch", branch="Artificial Intelligence and Data Science", graduation_year=2026)
        cohort2 = Cohort(org_id=org.id, name="B.Tech Computer Science - 2028 Batch", branch="Computer Science and Engineering", graduation_year=2028)
        db.add_all([cohort1, cohort2])
        db.flush()

        # 2. Careers
        print("💼 Seeding 13 Core Careers...")
        career_objs = {}
        for c in CAREERS_DATA:
            career = Career(
                slug=c["slug"],
                name=c["name"],
                plain_description=c["plain_description"],
                day_in_life=c["day_in_life"],
                typical_tasks=c["typical_tasks"],
                entry_titles=c["entry_titles"],
                growth_path=c["growth_path"],
                demand_level=c["demand_level"],
                salary_range_note=c["salary_range_note"],
                suits_who=c["suits_who"],
                mini_project=c["mini_project"]
            )
            db.add(career)
            db.flush()
            career_objs[c["slug"]] = career

        # 3. Skills
        print("🧠 Seeding 85+ Skills with Beginner Guides...")
        skill_objs = {}
        for s in ALL_SKILLS_DATA:
            skill = Skill(
                slug=s["slug"],
                name=s["name"],
                category=s["category"],
                plain_explanation=s["plain_explanation"],
                prerequisites=s["prerequisites"],
                estimated_hours_per_level=s["estimated_hours_per_level"],
                difficulty=s["difficulty"],
                common_mistakes=s["common_mistakes"],
                done_criteria=s["done_criteria"],
                learning_method=s["learning_method"]
            )
            db.add(skill)
            db.flush()
            skill_objs[s["slug"]] = skill

        # 4. Career-Skill Relationships
        print("🔗 Mapping Career Requirements & Target Levels...")
        for career_slug, req_skills in CAREER_SKILLS_MAP.items():
            if career_slug in career_objs:
                c_id = career_objs[career_slug].id
                for skill_slug, target_lvl, weight in req_skills:
                    if skill_slug in skill_objs:
                        cs = CareerSkill(
                            career_id=c_id,
                            skill_id=skill_objs[skill_slug].id,
                            target_level=target_lvl,
                            weight=weight
                        )
                        db.add(cs)
        db.flush()

        # 5. Resources
        print("📚 Seeding Reputable Learning Resources...")
        for r in ALL_RESOURCES_DATA:
            if r["skill_slug"] in skill_objs:
                res = Resource(
                    title=r["title"],
                    type=r["type"],
                    url=r["url"],
                    skill_id=skill_objs[r["skill_slug"]].id,
                    difficulty=r["difficulty"],
                    duration=r["duration"],
                    provider=r["provider"],
                    free=r["free"]
                )
                db.add(res)
        db.flush()

        # 6. Glossary
        print("📖 Seeding 100+ Plain-Language Glossary Terms...")
        for g in GLOSSARY_DATA:
            item = Glossary(
                term=g["term"],
                category=g["category"],
                plain_meaning=g["plain_meaning"],
                example=g.get("example", "")
            )
            db.add(item)
        db.flush()

        # 7. Assessments
        print("📝 Seeding Assessment MCQs & Practical Tasks...")
        for skill_slug, a_data in ASSESSMENTS_DATA.items():
            if skill_slug in skill_objs:
                assessment = Assessment(
                    skill_id=skill_objs[skill_slug].id,
                    title=a_data["title"],
                    description=a_data["description"],
                    target_level=a_data["target_level"],
                    questions=a_data["questions"],
                    practical_task=a_data["practical_task"]
                )
                db.add(assessment)
        db.flush()

        # 8. Demo Learners & Admin
        print("👥 Seeding 4 Demo Learners & Admin...")
        users_meta = [
            {
                "email": "arif@skillpath.dev",
                "password": "arif123",
                "role": "learner",
                "full_name": "Arif Mohamed",
                "education": "B.Tech",
                "branch": "Artificial Intelligence and Data Science",
                "year": 3,
                "institution": "National Institute of Technology",
                "interests": ["building", "teaching machines", "finding patterns"],
                "strengths": ["math", "logical thinking"],
                "career_goal": "",
                "goal_status": "unknown",
                "weekly_hours": 8.0,
                "cohort_id": cohort1.id,
                "initial_skills": []
            },
            {
                "email": "priya@skillpath.dev",
                "password": "priya123",
                "role": "learner",
                "full_name": "Priya Sharma",
                "education": "B.Tech",
                "branch": "Computer Science and Engineering",
                "year": 1,
                "institution": "City Engineering College",
                "interests": ["creative design", "building apps"],
                "strengths": ["creative problem solving"],
                "career_goal": "",
                "goal_status": "unknown",
                "weekly_hours": 6.0,
                "cohort_id": cohort2.id,
                "initial_skills": []
            },
            {
                "email": "rohan@skillpath.dev",
                "password": "rohan123",
                "role": "learner",
                "full_name": "Rohan Patel",
                "education": "B.Tech",
                "branch": "Information Technology",
                "year": 2,
                "institution": "State Technical University",
                "interests": ["building websites", "databases"],
                "strengths": ["coding", "debugging"],
                "career_goal": "Full Stack Developer",
                "goal_status": "known",
                "weekly_hours": 10.0,
                "cohort_id": cohort1.id,
                "initial_skills": [
                    ("python-basics", 2),
                    ("sql-basics", 2),
                    ("html-css", 1)
                ]
            },
            {
                "email": "ananya@skillpath.dev",
                "password": "ananya123",
                "role": "learner",
                "full_name": "Ananya Sen",
                "education": "B.Com",
                "branch": "Commerce and Finance",
                "year": 4,
                "institution": "National Commerce College",
                "interests": ["business metrics", "spreadsheets"],
                "strengths": ["financial analysis", "communication"],
                "career_goal": "Data Analyst",
                "goal_status": "rough",
                "weekly_hours": 12.0,
                "cohort_id": None,
                "initial_skills": [
                    ("sql-basics", 1),
                    ("data-visualization", 1)
                ]
            },
            {
                "email": "admin@skillpath.dev",
                "password": "admin123",
                "role": "admin",
                "full_name": "SkillPath System Admin",
                "education": "M.Tech",
                "branch": "Computer Science",
                "year": 0,
                "institution": "SkillPath University Alliance",
                "interests": ["education", "curriculum planning"],
                "strengths": ["administration", "analytics"],
                "career_goal": "System Director",
                "goal_status": "known",
                "weekly_hours": 40.0,
                "cohort_id": None,
                "initial_skills": []
            }
        ]

        for u in users_meta:
            user = User(
                email=u["email"],
                hashed_password=get_password_hash(u["password"]),
                role=u["role"],
                is_active=True
            )
            db.add(user)
            db.flush()

            profile = Profile(
                user_id=user.id,
                full_name=u["full_name"],
                education=u["education"],
                branch=u["branch"],
                year=u["year"],
                institution=u["institution"],
                interests=u["interests"],
                strengths=u["strengths"],
                career_goal=u["career_goal"],
                goal_status=u["goal_status"],
                weekly_hours=u["weekly_hours"],
                cohort_id=u["cohort_id"],
                learner_pace_factor=1.0
            )
            db.add(profile)

            # Create default SkillPassport for each learner
            slug_part = u["full_name"].lower().replace(" ", "-") + f"-{user.id:04d}"
            passport = SkillPassport(
                user_id=user.id,
                slug=slug_part,
                is_public=True,
                show_scores=True,
                show_evidence=True
            )
            db.add(passport)

            # Add any initial skills
            for s_slug, s_lvl in u["initial_skills"]:
                if s_slug in skill_objs:
                    usk = UserSkill(
                        user_id=user.id,
                        skill_id=skill_objs[s_slug].id,
                        level=s_lvl,
                        confidence=0.8,
                        source="self"
                    )
                    db.add(usk)

        seed_practice_questions(db)

        db.commit()
        print("✅ Database successfully seeded with production data!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error during seed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
