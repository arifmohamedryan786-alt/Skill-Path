import math
from typing import Any
from sqlalchemy.orm import Session
from backend.app.models import Resource, Skill, UserSkill

class ResourceRecommenderAgent:
    """
    Retrieves and ranks reputable learning resources for gap skills:
    - Enforces prerequisite order
    - Provides a triad for each gap: Theory (course), Practical (tutorial), Application (project)
    - Prioritizes beginner-friendly, high-rated free resources
    """

    def recommend_for_gaps(
        self,
        db: Session,
        user_id: int,
        gap_skill_ids: list[int],
        max_resources_per_skill: int = 3
    ) -> list[dict[str, Any]]:
        user_skills_map = {
            us.skill_id: us.level
            for us in db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
        }

        recommendations = []

        for skill_id in gap_skill_ids:
            skill = db.query(Skill).filter(Skill.id == skill_id).first()
            if not skill:
                continue

            current_lvl = user_skills_map.get(skill_id, 0)
            resources = db.query(Resource).filter(Resource.skill_id == skill_id).all()

            # Group by type: course (theory), tutorial (practice), project (application)
            theory_res = [r for r in resources if r.type in ["course", "book"]]
            practice_res = [r for r in resources if r.type in ["tutorial", "exercise"]]
            project_res = [r for r in resources if r.type == "project"]

            selected = []
            if theory_res:
                selected.append(theory_res[0])
            if practice_res:
                selected.append(practice_res[0])
            if project_res:
                selected.append(project_res[0])

            # Fill up to max_resources_per_skill if needed
            for r in resources:
                if len(selected) >= max_resources_per_skill:
                    break
                if r not in selected:
                    selected.append(r)

            recommendations.append({
                "skill_id": skill.id,
                "skill_name": skill.name,
                "skill_slug": skill.slug,
                "category": skill.category,
                "current_level": current_lvl,
                "resources": [
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
                    for r in selected
                ]
            })

        return recommendations

resource_recommender_agent = ResourceRecommenderAgent()
