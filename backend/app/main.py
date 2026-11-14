import logging
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.app.config import settings
from backend.app.database import engine, Base, get_db
from backend.app.seed.seed_runner import seed_database
from backend.app.agents.llm_client import llm_client
from backend.app.api import (
    auth, profile, discovery, careers, skills, roadmap,
    simulator, assessments, passport, interview, guide,
    mentor, admin, general, i18n, practice
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("skillpath")

# Initialize FastAPI App
app = FastAPI(
    title="SkillPath API",
    description="Your Career Path, From Zero to Job-Ready – Production REST API & Multi-Agent Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event: ensure database schema and seed data exist
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_database()
    active_model = llm_client.get_model()
    provider = llm_client.provider
    active_status = "Connected" if llm_client.is_available else "Offline Fallback Mode"
    log_line = f"🚀 SkillPath API ready | Active LLM Provider: {provider} | Model: {active_model} | Status: {active_status}"
    logger.info(log_line)
    print(log_line)

# Include Routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(discovery.router)
app.include_router(careers.router)
app.include_router(skills.router)
app.include_router(roadmap.router)
app.include_router(simulator.router)
app.include_router(assessments.router)
app.include_router(passport.router)
app.include_router(interview.router)
app.include_router(guide.router)
app.include_router(mentor.router)
app.include_router(admin.router)
app.include_router(general.router)
app.include_router(i18n.router)
app.include_router(practice.router)

@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    db_ok = True
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False
    return {
        "status": "healthy" if db_ok else "unhealthy",
        "app": settings.PROJECT_NAME,
        "database": "connected" if db_ok else "disconnected",
        "version": "1.0.0",
        "llm_provider": llm_client.provider,
        "llm_connected": llm_client.is_available
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to SkillPath – Your Career Path, From Zero to Job-Ready API",
        "docs": "/docs",
        "health": "/health"
    }

