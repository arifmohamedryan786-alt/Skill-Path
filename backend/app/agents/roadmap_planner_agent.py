from datetime import datetime, timedelta
from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import (
    RoadmapStage, RoadmapItem, WeeklySprint, Career, CareerSkill,
    UserSkill, Skill, Profile
)

class RoadmapPlannerAgent:
    """
    Builds the complete 7-stage zero-to-job roadmap:
    1 Explore -> 2 Foundations -> 3 Core skills -> 4 Projects -> 5 Internships -> 6 Interview prep -> 7 Growth
    Adjusts milestones based on student's year of study (1st, 2nd, 3rd, 4th year).
    """

    STAGES_TEMPLATE = [
        (1, "1 Explore & Align", "Understand career paths, clarify your interests, and validate your direction with small mini-projects.", 2),
        (2, "2 Foundations", "Master core programming syntax, command line tools, Git version control, and essential math.", 4),
        (3, "3 Core Domain Skills", "Deep-dive into role-specific frameworks, databases, and algorithms required for everyday work.", 8),
        (4, "4 Projects & Portfolio", "Build 3 polished, real-world portfolio projects and document your code thoroughly on GitHub.", 6),
        (5, "5 Internships & Experience", "Target industry internships, open-source contributions, hackathons, and craft your resume.", 8),
        (6, "6 Interview Prep & Applications", "Conduct mock technical and behavioral interviews, solve coding challenges, and apply to companies.", 6),
        (7, "7 Growth & Specialization", "Pursue advanced industry certifications, leadership roles, or higher studies (GATE, GRE, MS, MBA).", 12)
    ]

    def build_or_rebuild_roadmap(
        self,
        db: Session,
        user_id: int,
        target_career_slug: str
    ) -> list[RoadmapStage]:
        # 1. Clear existing roadmap stages and items for clean rebuild
        db.query(RoadmapItem).filter(RoadmapItem.user_id == user_id).delete()
        db.query(RoadmapStage).filter(RoadmapStage.user_id == user_id).delete()
        db.flush()

        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        student_year = profile.year if profile else 3
        weekly_hours = profile.weekly_hours if profile else 8.0

        career = db.query(Career).filter(Career.slug == target_career_slug).first()
        if not career:
            career = db.query(Career).first()

        career_skills = db.query(CareerSkill).filter(CareerSkill.career_id == career.id).all()
        user_skills_map = {
            us.skill_id: us.level
            for us in db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
        }

        # Segregate required skills by level and category
        foundation_skills = []
        core_skills = []

        for cs in career_skills:
            skill = db.query(Skill).filter(Skill.id == cs.skill_id).first()
            if not skill:
                continue
            cur_lvl = user_skills_map.get(skill.id, 0)
            if skill.category in ["Programming", "Testing"] and "basics" in skill.slug:
                foundation_skills.append((skill, cs.target_level, cur_lvl))
            else:
                core_skills.append((skill, cs.target_level, cur_lvl))

        # Create the 7 Stages
        created_stages = []
        for stage_num, title, desc, base_weeks in self.STAGES_TEMPLATE:
            # Stage status logic
            if stage_num == 1:
                status = "completed"
            elif stage_num == 2:
                # If foundations already mastered, mark completed
                all_foundations_done = all(cur >= tgt for _, tgt, cur in foundation_skills) if foundation_skills else False
                status = "completed" if all_foundations_done else "current"
            elif stage_num == 3:
                status = "current" if created_stages[1].status == "completed" else "locked"
            else:
                status = "locked"

            stage = RoadmapStage(
                user_id=user_id,
                stage_number=stage_num,
                title=title,
                description=desc,
                status=status,
                est_weeks=base_weeks
            )
            db.add(stage)
            db.flush()
            created_stages.append(stage)

        # Populate Items per stage
        # Stage 1: Explore
        item_1_1 = RoadmapItem(
            stage_id=created_stages[0].id,
            user_id=user_id,
            title="Complete Career Discovery Assessment",
            description="Take the 15-question interest and strengths assessment to discover top matching roles.",
            item_type="milestone",
            order=1,
            status="completed",
            due_week=1,
            est_hours=1.0,
            completed_at=datetime.utcnow()
        )
        item_1_2 = RoadmapItem(
            stage_id=created_stages[0].id,
            user_id=user_id,
            title=f"Complete 1-Hour Try-It Mini Project for {career.name}",
            description=career.mini_project.get("title", "Run your first mini-project"),
            item_type="project",
            order=2,
            status="completed" if profile and profile.career_goal else "pending",
            due_week=1,
            est_hours=1.5
        )
        db.add_all([item_1_1, item_1_2])

        # Stage 2: Foundations
        f_order = 1
        for sk, tgt, cur in foundation_skills:
            item = RoadmapItem(
                stage_id=created_stages[1].id,
                user_id=user_id,
                skill_id=sk.id,
                title=f"Master {sk.name} (Reach Level {tgt})",
                description=sk.plain_explanation,
                item_type="skill",
                order=f_order,
                status="completed" if cur >= tgt else ("in_progress" if cur > 0 else "pending"),
                due_week=max(1, f_order * 2),
                est_hours=sk.estimated_hours_per_level * max(1, tgt - cur)
            )
            db.add(item)
            f_order += 1

        # Stage 3: Core Domain Skills
        c_order = 1
        for sk, tgt, cur in core_skills:
            item = RoadmapItem(
                stage_id=created_stages[2].id,
                user_id=user_id,
                skill_id=sk.id,
                title=f"Master {sk.name} (Reach Level {tgt})",
                description=sk.plain_explanation,
                item_type="skill",
                order=c_order,
                status="completed" if cur >= tgt else "pending",
                due_week=4 + (c_order * 2),
                est_hours=sk.estimated_hours_per_level * max(1, tgt - cur)
            )
            db.add(item)
            c_order += 1

        # Stage 4: Projects & Portfolio
        item_4_1 = RoadmapItem(
            stage_id=created_stages[3].id,
            user_id=user_id,
            title="Beginner Portfolio Project: Real-world Prototype",
            description=f"Build and document a standalone {career.name} project demonstrating core APIs and data pipelines.",
            item_type="project",
            order=1,
            status="pending",
            due_week=12,
            est_hours=15.0
        )
        item_4_2 = RoadmapItem(
            stage_id=created_stages[3].id,
            user_id=user_id,
            title="Capstone Full-Stack Production Project",
            description="Build an end-to-end full system with authentication, clean UI, automated testing, and Docker containerization.",
            item_type="project",
            order=2,
            status="pending",
            due_week=16,
            est_hours=25.0
        )
        db.add_all([item_4_1, item_4_2])

        # Stage 5: Internships & Experience (Adjusted by Year of Study)
        internship_note = ""
        if student_year == 1:
            internship_note = "Year 1 focus: Focus on open-source contributions, college tech clubs, and build your foundational GitHub profile."
        elif student_year == 2:
            internship_note = "Year 2 focus: Apply for winter/summer internships, participate in 48-hour hackathons, and network with alumni."
        elif student_year == 3:
            internship_note = "Year 3 focus: Critical campus placement prep! Target 2-month summer internships (apply 6 months ahead in Oct-Jan)."
        else:
            internship_note = "Year 4 focus: Full-time campus placement drives, direct company referrals, and off-campus applications."

        item_5_1 = RoadmapItem(
            stage_id=created_stages[4].id,
            user_id=user_id,
            title=f"Internship Search Strategy ({internship_note})",
            description=f"Curate a target list of 20 companies hiring {career.name} interns and apply with customized cover letters.",
            item_type="internship",
            order=1,
            status="pending",
            due_week=18,
            est_hours=10.0
        )
        item_5_2 = RoadmapItem(
            stage_id=created_stages[4].id,
            user_id=user_id,
            title="LinkedIn & GitHub Portfolio Polish",
            description="Write comprehensive READMEs, pin top 3 projects, add live demo URLs, and write 3 technical summary posts.",
            item_type="milestone",
            order=2,
            status="pending",
            due_week=20,
            est_hours=8.0
        )
        db.add_all([item_5_1, item_5_2])

        # Stage 6: Interview Prep
        item_6_1 = RoadmapItem(
            stage_id=created_stages[5].id,
            user_id=user_id,
            title=f"Mock Interview Simulator Sessions for {career.name}",
            description="Complete 3 mock technical interview sessions using SkillPath's Mock Interview Coach with rubric scoring.",
            item_type="milestone",
            order=1,
            status="pending",
            due_week=22,
            est_hours=6.0
        )
        item_6_2 = RoadmapItem(
            stage_id=created_stages[5].id,
            user_id=user_id,
            title="Behavioral STAR Method & System Design Practice",
            description="Prepare 5 STAR stories covering team conflicts, tight deadlines, and technical debugging triumphs.",
            item_type="milestone",
            order=2,
            status="pending",
            due_week=24,
            est_hours=8.0
        )
        db.add_all([item_6_1, item_6_2])

        # Stage 7: Growth & Certifications
        item_7_1 = RoadmapItem(
            stage_id=created_stages[6].id,
            user_id=user_id,
            title="Industry Credential & Verified Skill Passport",
            description="Pass all SkillPath checkpoint assessments at 70%+ to unlock tamper-evident SHA-256 verified badges.",
            item_type="certification",
            order=1,
            status="pending",
            due_week=26,
            est_hours=10.0
        )
        item_7_2 = RoadmapItem(
            stage_id=created_stages[6].id,
            user_id=user_id,
            title="Long-Term Specialization & Higher Studies Planning",
            description="Evaluate specialization paths (Deep Learning, MLOps, Cloud Architecture) and exams (GATE, GRE) if pursuing MS.",
            item_type="milestone",
            order=2,
            status="pending",
            due_week=28,
            est_hours=5.0
        )
        db.add_all([item_7_1, item_7_2])

        db.commit()
        return created_stages

roadmap_planner_agent = RoadmapPlannerAgent()

