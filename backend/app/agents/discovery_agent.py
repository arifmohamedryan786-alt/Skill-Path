from typing import Any
from backend.app.seed.seed_discovery_questions import DISCOVERY_QUESTIONS
from backend.app.seed.seed_data import BRANCH_CAREER_MAPPINGS
from backend.app.agents.llm_client import llm_client

class DiscoveryAgent:
    """
    Ranks careers based on learner interests, subject preferences, work style,
    and mini try-it aptitude questions, providing plain-language explanations.
    """

    def get_questions(self) -> list[dict[str, Any]]:
        # Return questions without exposing internal weights to client
        client_questions = []
        for q in DISCOVERY_QUESTIONS:
            clean_opts = []
            for opt in q["options"]:
                clean_opts.append({
                    "value": opt["value"],
                    "label": opt["label"]
                })
            client_questions.append({
                "id": q["id"],
                "category": q["category"],
                "question": q["question"],
                "help_text": q["help_text"],
                "type": q["type"],
                "options": clean_opts
            })
        return client_questions

    def evaluate_answers(
        self,
        answers: dict[str, Any],
        student_branch: str = "",
        student_year: int = 1
    ) -> dict[str, Any]:
        """
        Deterministic scoring algorithm:
        1. Accumulates career points from chosen question options
        2. Applies branch alignment bonus (e.g. AI & DS gets bonus for AI/ML and Data careers)
        3. Normalizes match percentages between 65% and 95%
        4. Selects top 5 ranked careers with plain-language reasons
        """
        career_scores: dict[str, float] = {
            "ai-ml-engineer": 10.0,
            "data-analyst": 10.0,
            "data-scientist": 10.0,
            "data-engineer": 10.0,
            "full-stack-developer": 10.0,
            "frontend-developer": 10.0,
            "cloud-engineer": 10.0,
            "devops-engineer": 10.0,
            "cybersecurity-analyst": 10.0,
            "ui-ux-designer": 10.0,
            "mobile-app-developer": 10.0,
            "software-tester-qa": 10.0,
            "product-analyst": 10.0
        }

        aptitude_scores = {
            "analytical": 50.0,
            "creative": 50.0,
            "engineering": 50.0,
            "investigative": 50.0
        }

        # 1. Evaluate options
        for q in DISCOVERY_QUESTIONS:
            q_id = str(q["id"])
            if q_id in answers:
                selected_val = answers[q_id]
                for opt in q["options"]:
                    if opt["value"] == selected_val:
                        weights = opt.get("weights", {})
                        for c_slug, pts in weights.items():
                            if c_slug in career_scores:
                                career_scores[c_slug] += pts * 5.0
                        
                        # Category-based aptitude boosts
                        if q["category"] == "aptitude":
                            aptitude_scores["analytical"] += 15.0
                        elif q["category"] == "enjoyment" and "design" in selected_val:
                            aptitude_scores["creative"] += 15.0
                        elif q["category"] == "enjoyment" and "build" in selected_val:
                            aptitude_scores["engineering"] += 15.0
                        elif q["category"] == "work_style" and "investigative" in selected_val:
                            aptitude_scores["investigative"] += 15.0

        # 2. Branch Alignment Bonus
        matched_branch_careers = []
        for branch_key, mapped_careers in BRANCH_CAREER_MAPPINGS.items():
            if branch_key.lower() in student_branch.lower() or student_branch.lower() in branch_key.lower():
                matched_branch_careers = mapped_careers
                for c_slug in mapped_careers:
                    if c_slug in career_scores:
                        career_scores[c_slug] += 18.0
                break

        # 3. Sort and pick top 5
        sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
        top_5_items = sorted_careers[:5]

        # Normalize top score to ~94%, fifth to ~70%
        highest_score = max(top_5_items[0][1], 1.0)
        
        reasons_map = {
            "ai-ml-engineer": f"You enjoy teaching machines and finding mathematical patterns in numbers{' and your background in ' + student_branch + ' provides strong mathematical foundations' if student_branch else ''}.",
            "data-analyst": "You like finding patterns in real-world data and translating spreadsheet numbers into clear charts that guide decisions.",
            "data-scientist": "You have a natural curiosity for probability and statistical inquiry, and like digging deep into unknown data.",
            "data-engineer": "You enjoy organizing systems, backend data plumbing, and ensuring large pipelines run reliably.",
            "full-stack-developer": "You love building complete, working applications from scratch and seeing both the interface and backend come together.",
            "frontend-developer": "You have an eye for visual design and like making modern web interfaces that react immediately to user clicks.",
            "cloud-engineer": "You prefer working behind the scenes on scalable server infrastructure, networking, and cloud platforms.",
            "devops-engineer": "You value automation and enjoy building continuous deployment pipelines that eliminate repetitive manual steps.",
            "cybersecurity-analyst": "You have an investigative detective mindset and enjoy protecting digital systems and finding security flaws.",
            "ui-ux-designer": "You are deeply empathetic, creative, and love designing intuitive screens and frictionless user flows.",
            "mobile-app-developer": "You love smartphones and want to build interactive apps that people carry in their pockets every day.",
            "software-tester-qa": "You have sharp attention to detail, enjoy asking 'what could break here?', and care about rock-solid quality.",
            "product-analyst": "You enjoy analyzing user behavior, product conversion funnels, and identifying what features to build next."
        }

        results = []
        for idx, (c_slug, score) in enumerate(top_5_items):
            # Graduated percentage scale
            pct = round(min(94.0 - (idx * 5.0) + (score % 3), 96.0), 1)
            results.append({
                "slug": c_slug,
                "match_pct": pct,
                "reason": reasons_map.get(c_slug, "Your interests and logical reasoning align strongly with this career path.")
            })

        summary = f"Based on your answers{' and degree in ' + student_branch if student_branch else ''}, your top career match is {results[0]['slug'].replace('-', ' ').title()} ({results[0]['match_pct']}% match)."

        return {
            "top_careers": results,
            "aptitude_scores": {k: min(round(v, 1), 95.0) for k, v in aptitude_scores.items()},
            "summary_message": summary
        }

discovery_agent = DiscoveryAgent()

