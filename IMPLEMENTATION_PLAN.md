# SkillPath – Implementation Plan & Architecture

SkillPath is an AI-powered, beginner-first career discovery and personalized learning platform. It empowers students with zero direction to discover tailored careers, analyze skill gaps, generate actionable 7-stage roadmaps, simulate time-to-job-readiness, prepare for interviews, and earn tamper-evident skill passports.

## 1. Architecture Overview

```
                               +------------------------------------------+
                               |              Frontend (SPA)              |
                               | React + Vite + TypeScript + Tailwind CSS |
                               |  Recharts + Lucide + i18next + QR / PDF  |
                               +--------------------+---------------------+
                                                    | REST / SSE
                                                    v
                               +------------------------------------------+
                               |            Backend API Server            |
                               |         FastAPI + Pydantic v2            |
                               |    Auth (JWT) + SQLite (SQLAlchemy)      |
                               +--------------------+---------------------+
                                                    |
                     +------------------------------+------------------------------+
                     |                                                             |
                     v                                                             v
+------------------------------------------+             +------------------------------------------+
|          LangGraph Orchestrator          |             |       Vector & Semantic Retrieval        |
|  13 Specialized Agents + Event Routing   |             |  Embeddings + Cosine / FAISS Similarity  |
|  Robust Rule-based Fallback Engine       |             |  200+ Seeded Verified Learning Resources |
+------------------------------------------+             +------------------------------------------+
```

## 2. Phased Roadmap

### Phase 1: Foundation & Design System
- Setup workspace layout: `/backend` and `/frontend`.
- Define Tailwind design tokens matching specifications:
  - Background `#F7F6F2`, Surface `#FFFFFF`, Ink `#1C2B2A`, Secondary `#5E6B69`, Border `#E3E1DA`
  - Primary `#0F6E68`, Primary Tint `#E3F1EF`, Accent `#E8A33D`, Success `#2F8F5B`, Warning `#D9822B`, Danger `#C8463D`.
  - Typography: Serif headings (Fraunces / DM Serif) and Clean Sans body (Plus Jakarta Sans / Inter).

### Phase 2: Backend Architecture & Database Models
- SQLAlchemy models:
  - `User`, `Profile`, `DiscoveryResponse`, `CareerShortlist`, `Career`, `CareerSkill`, `Skill`, `UserSkill`
  - `Resource`, `RoadmapStage`, `RoadmapItem`, `WeeklySprint`, `Scenario`, `ForecastSnapshot`
  - `Assessment`, `AssessmentResult`, `SkillPassport`, `VerifiedSkill`, `InterviewSession`
  - `AgentLog`, `ChatMessage`, `Glossary`, `Organization`, `Cohort`
- Comprehensive seed database:
  - 13 distinct careers (AI/ML Engineer, Data Analyst, Data Scientist, Full Stack Developer, Frontend Developer, Data Engineer, Cloud Engineer, DevOps Engineer, Cybersecurity Analyst, UI/UX Designer, Mobile App Developer, Software QA Tester, Product Analyst).
  - 85+ skills with plain-language explanations, difficulty, prerequisites, common mistakes, done criteria.
  - 210+ reputable resources with type, difficulty, provider, free flag, and duration.
  - 100+ plain-language glossary entries.
  - Branch-to-career mappings (e.g. B.Tech AI & DS -> AI/ML, Data Science, Data Analyst, Data Engineering).
  - 4 realistic demo learners (including Arif Mohamed) + 1 admin.

### Phase 3: LangGraph Multi-Agent Architecture
- 13 autonomous agent modules with strict Pydantic output validation:
  1. `Discovery Agent`: 15-question interest/strength assessment & matching with plain-language explanations.
  2. `Profile Agent`: Resume extraction with prompt injection defense.
  3. `Skill Analyst Agent`: Gap analysis, strength/weakness synthesis.
  4. `Career Matcher Agent`: Weighted match calculation, readiness tiering.
  5. `Learning Coach Agent`: "How to learn this" cards & Day-by-Day "First Week" sprint.
  6. `Resource Recommender Agent`: Semantic retrieval with prerequisite enforcement.
  7. `Roadmap Planner Agent`: 7-stage progression (Explore to Growth), timeline adjustment by year of study.
  8. `Assessment Agent`: 5-MCQ + 1 practical task generator, auto-grading, level updating.
  9. `Progress Evaluator Agent`: Velocity calculation, `learner_pace_factor` dynamic tracking.
  10. `Simulation Agent`: Flight simulator forecast, optimistic/realistic dates, scenario planning.
  11. `Interview Coach Agent`: Mock interview questions, rubric grading (correctness, depth, clarity, examples 1-5).
  12. `Career Guide Agent`: Comprehensive end-to-end PDF/guide generator.
  13. `AI Mentor Agent`: Real-time streaming chat, tool execution, session memory, proactive nudges.
- LangGraph Orchestrator with event hooks and explainable `AgentLog` auditing.
- Complete rule-based deterministic fallback when no LLM key is configured.

### Phase 4: REST API & Business Logic
- Auth: JWT login, registration, password hashing, role enforcement (`learner`, `admin`).
- Endpoints covering all 35+ routes required in Section 10.
- SHA-256 cryptographic verification for Skill Passports.
- SSE endpoint for AI Mentor streaming.

### Phase 5: Frontend Application (SPA)
- Responsive layout (360px to 1440px) with custom line-art SVGs, sidebar, top bar with current goal & progress.
- Pages:
  - `Login/Register` & Role Switcher
  - Beginner-first Onboarding Wizard (Goal status check -> 5-step wizard)
  - Career Discovery Engine & Career Explorer ("Day in the life", comparison, "Try before you choose" mini-tasks)
  - Student Dashboard (clean human summary, top matches, first week tasks, roadmap preview)
  - 7-Stage Roadmap Journey Map with "How to Learn This" drawers
  - Skill Analysis with Radar Chart & Gap Bars
  - Career Flight Simulator with Interactive Hours Slider, What-If scenarios & Apply Plan
  - Verified Skill Passport with SHA-256 verification, QR Code, Privacy Toggles, PDF Export
  - Mock Interview Coach with text & Web Speech API voice input, rubric breakdown, trend chart
  - Comprehensive Career Guide viewer & export
  - AI Mentor slide-over and dedicated page with quick prompt chips
  - Organization / University Admin Cohort Dashboard
  - Plain-language Glossary tooltips across all technical terms
  - Multilingual support (English, Hindi, Tamil) via i18next

### Phase 6: Automated Testing & Verification
- Pytest suite testing:
  - Career matching algorithm and weighted scoring
  - Discovery scoring and recommendation logic
  - Forecast calculation and dynamic `learner_pace_factor`
  - Tamper-evident SHA-256 passport verification
  - Adaptive rules (failing assessment inserts remedial items, passing triggers passport verification)
  - API endpoint integration tests
- Frontend test coverage / typecheck & build validation.

### Phase 7: Deployment & Documentation
- `Dockerfile`, `docker-compose.yml`, `Makefile`, `.env.example`.
- In-depth `README.md` with architecture diagrams, API docs, formula explanations, and 5-minute live pitch & demo script.

