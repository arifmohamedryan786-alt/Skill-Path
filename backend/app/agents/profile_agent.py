import re
from typing import Any
from backend.app.agents.llm_client import llm_client, sanitize_user_input

class ProfileAgent:
    """
    Extracts skills, projects, certifications, and educational milestones
    from pasted resume text or portfolios.
    """

    KNOWN_SKILL_PATTERNS = {
        "Python": ["python", "python3", "py"],
        "SQL": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
        "JavaScript": ["javascript", "js", "es6"],
        "TypeScript": ["typescript", "ts"],
        "React": ["react", "react.js", "reactjs"],
        "HTML/CSS": ["html", "css", "html5", "css3", "tailwind"],
        "FastAPI": ["fastapi", "flask", "django"],
        "Machine Learning": ["machine learning", "scikit-learn", "sklearn", "ml"],
        "Deep Learning": ["deep learning", "neural network", "pytorch", "tensorflow"],
        "Pandas": ["pandas", "numpy"],
        "Data Visualization": ["matplotlib", "seaborn", "tableau", "power bi"],
        "Git": ["git", "github", "gitlab"],
        "Docker": ["docker", "container"],
        "AWS": ["aws", "s3", "ec2", "lambda", "cloud"]
    }

    async def parse_resume(self, raw_resume_text: str) -> dict[str, Any]:
        clean_text = sanitize_user_input(raw_resume_text)

        # 1. Try LLM if available
        if llm_client.is_available:
            system_prompt = (
                "You are an expert technical resume parser for SkillPath. "
                "Extract technical skills, completed projects (title, description), "
                "education degree, and branch. Output strictly JSON with keys: "
                "extracted_skills (list of strings), extracted_projects (list of objects with title and description), "
                "extracted_education (string or null), extracted_branch (string or null), summary (short string)."
            )
            try:
                result = await llm_client.json(prompt=clean_text, system_prompt=system_prompt)
                if result and "extracted_skills" in result:
                    return result
            except Exception:
                pass # Falls back cleanly to deterministic rule-based extraction

        # 2. Deterministic Rule-Based Extraction Fallback
        extracted_skills = []
        lower_text = clean_text.lower()
        for skill_name, aliases in self.KNOWN_SKILL_PATTERNS.items():
            for alias in aliases:
                # Word boundary search
                if re.search(r"\b" + re.escape(alias) + r"\b", lower_text):
                    extracted_skills.append(skill_name)
                    break

        # Extract potential project headings
        extracted_projects = []
        lines = [line.strip() for line in clean_text.split("\n") if line.strip()]
        for idx, line in enumerate(lines):
            if any(kw in line.lower() for kw in ["project", "developed", "built", "implemented"]):
                if len(line) < 80:
                    desc = lines[idx + 1] if idx + 1 < len(lines) else ""
                    extracted_projects.append({
                        "title": line.strip("#-* "),
                        "description": desc[:200]
                    })
                    if len(extracted_projects) >= 3:
                        break

        # Detect education
        extracted_education = "B.Tech" if "b.tech" in lower_text or "bachelor" in lower_text else "Undergraduate"
        extracted_branch = ""
        if "artificial intelligence" in lower_text or "data science" in lower_text:
            extracted_branch = "Artificial Intelligence and Data Science"
        elif "computer science" in lower_text:
            extracted_branch = "Computer Science and Engineering"
        elif "information technology" in lower_text:
            extracted_branch = "Information Technology"

        summary = f"Parsed {len(extracted_skills)} technical skills and {len(extracted_projects)} projects from your profile."

        return {
            "extracted_skills": list(set(extracted_skills)),
            "extracted_projects": extracted_projects,
            "extracted_education": extracted_education,
            "extracted_branch": extracted_branch,
            "extracted_year": 3 if "3rd" in lower_text or "third" in lower_text else 1,
            "summary": summary
        }

profile_agent = ProfileAgent()

