import math
from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import Skill, Resource, Profile, Career

class LearningCoachAgent:
    """
    Produces beginner-first 'How to learn this' cards with time estimates,
    learning methods (watch/practice/build), resources in order, done criteria,
    and a personalized 'Your First Week' day-by-day sprint plan.
    """

    def generate_how_to_learn_card(
        self,
        db: Session,
        skill_id: int,
        user_weekly_hours: float = 8.0,
        user_current_level: int = 0,
        career_goal: str = ""
    ) -> dict[str, Any]:
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if not skill:
            return {}

        resources = db.query(Resource).filter(Resource.skill_id == skill_id).all()
        
        # Calculate time estimate
        levels_to_gain = max(1, 2 - user_current_level)
        total_hours = round(levels_to_gain * skill.estimated_hours_per_level * skill.difficulty, 1)
        weeks_needed = max(1, math.ceil(total_hours / max(user_weekly_hours, 1.0)))

        # Learning method split
        method = skill.learning_method or {
            "watch_pct": 25,
            "practice_pct": 55,
            "build_pct": 20,
            "first_step": "Open your editor and type your first line of code.",
            "tip": "Spend 70% of your time actively writing code rather than passively watching."
        }

        # Format resources in curated order: Course -> Tutorial -> Exercise -> Project -> Book
        type_priority = {"course": 1, "tutorial": 2, "exercise": 3, "project": 4, "book": 5}
        sorted_resources = sorted(
            [
                {
                    "id": r.id,
                    "title": r.title,
                    "type": r.type,
                    "url": r.url,
                    "difficulty": r.difficulty,
                    "duration": r.duration,
                    "provider": r.provider,
                    "free": r.free
                }
                for r in resources
            ],
            key=lambda x: type_priority.get(x["type"], 9)
        )

        why_it_matters = f"{skill.name} is essential for {career_goal if career_goal else 'tech careers'} because it empowers you to build reliable, scalable solutions without getting stuck on boilerplate."
        if "python" in skill.slug:
            why_it_matters = f"Python comes first because almost every AI tool, backend framework, and data pipeline is built with it."
        elif "sql" in skill.slug:
            why_it_matters = f"SQL is the universal language of databases; every company stores user and product data in SQL tables."

        return {
            "skill_id": skill.id,
            "slug": skill.slug,
            "name": skill.name,
            "category": skill.category,
            "plain_explanation": skill.plain_explanation,
            "why_it_matters": why_it_matters,
            "prerequisites": skill.prerequisites or [],
            "current_level": user_current_level,
            "target_level": 2,
            "estimated_hours": total_hours,
            "estimated_weeks": weeks_needed,
            "weekly_hours_assumed": user_weekly_hours,
            "learning_method": method,
            "recommended_first_step": method.get("first_step", "Start with the 1-hour crash course below."),
            "resources": sorted_resources,
            "common_mistakes": skill.common_mistakes or [],
            "done_criteria": skill.done_criteria or [],
            "mini_exercise": {
                "title": f"Practice Exercise: Hands-on with {skill.name}",
                "prompt": f"Write a small 10-line script or document demonstrating core {skill.name} syntax and submit it for checkpoint review.",
                "duration": "30 mins"
            }
        }

    def generate_first_week_plan(
        self,
        db: Session,
        user_id: int,
        focus_skill_slug: str = "python-basics",
        weekly_hours: float = 8.0
    ) -> dict[str, Any]:
        """
        Creates a concrete day-by-day sprint plan with 30-60 minute bite-sized tasks.
        """
        skill = db.query(Skill).filter(Skill.slug == focus_skill_slug).first()
        if not skill:
            skill = db.query(Skill).first()

        focus_title = skill.name if skill else "Foundational Programming"

        tasks = [
            {
                "day": "Monday",
                "duration_mins": 45,
                "title": f"Set Up Your Workspace & Run Your First {focus_title} Line",
                "description": "Install your coding editor (VS Code or browser sandbox) and complete the initial 'Hello World' step.",
                "action_url": "https://www.freecodecamp.org/",
                "completed": False
            },
            {
                "day": "Tuesday",
                "duration_mins": 45,
                "title": f"Core Syntax: Variables, Types & Simple Decisions",
                "description": f"Learn how {focus_title} stores numbers and text, and write 3 simple if-else statements.",
                "action_url": "https://exercism.org/",
                "completed": False
            },
            {
                "day": "Wednesday",
                "duration_mins": 60,
                "title": "Interactive Practice: Solve 3 Beginner Challenges",
                "description": "Put theory into practice by solving 3 bite-sized algorithmic challenges in the browser.",
                "action_url": "https://exercism.org/",
                "completed": False
            },
            {
                "day": "Thursday",
                "duration_mins": 45,
                "title": "Learn the Loop: Automating Repetitive Tasks",
                "description": "Write a loop that filters a list of 10 items and prints only the ones that match your rule.",
                "action_url": "https://www.learnpython.org/",
                "completed": False
            },
            {
                "day": "Friday",
                "duration_mins": 60,
                "title": "Build a Mini-Script & Test Edge Cases",
                "description": "Combine variables, loops, and functions to build a working mini-calculator or data cleaner.",
                "action_url": "https://github.com/",
                "completed": False
            },
            {
                "day": "Saturday",
                "duration_mins": 60,
                "title": "Checkpoint Quiz & Git Checkpoint",
                "description": "Take SkillPath's 5-minute checkpoint quiz to verify your retention and commit your work to GitHub.",
                "action_url": "/assessments",
                "completed": False
            },
            {
                "day": "Sunday",
                "duration_mins": 30,
                "title": "Reflection & Weekly Progress Review",
                "description": "Review what felt easy and what felt hard. Check in with your AI Mentor to set up next week's sprint.",
                "action_url": "/mentor",
                "completed": False
            }
        ]

        why_it_matters = f"{focus_title} is your primary starting block. Spending just 45 minutes a day builds consistent momentum without burnout."

        return {
            "focus_topic": focus_title,
            "why_it_matters": why_it_matters,
            "weekly_hours": weekly_hours,
            "tasks": tasks
        }

learning_coach_agent = LearningCoachAgent()

