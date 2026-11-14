from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User, Profile
from backend.app.models.discovery import DiscoveryResponse
from backend.app.models.career import Career
from backend.app.models.agent_log import AgentLog
from backend.app.schemas.discovery import DiscoveryQuestion, DiscoverySubmitRequest, DiscoveryResultResponse, CareerMatchResult
from backend.app.api.deps import get_current_user
from backend.app.agents.discovery_agent import discovery_agent
from backend.app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/discovery", tags=["Career Discovery"])

@router.get("/questions", response_model=list[DiscoveryQuestion])
def get_discovery_questions():
    return discovery_agent.get_questions()

@router.post("/submit", response_model=DiscoveryResultResponse)
def submit_discovery_answers(
    submit_req: DiscoverySubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    branch = profile.branch if profile else ""
    year = profile.year if profile else 1

    eval_result = discovery_agent.evaluate_answers(
        answers=submit_req.answers,
        student_branch=branch,
        student_year=year
    )

    # Resolve Career IDs & details
    top_career_results = []
    top_careers_raw = eval_result["top_careers"]

    for item in top_careers_raw:
        c_slug = item["slug"]
        career = db.query(Career).filter(Career.slug == c_slug).first()
        if career:
            top_career_results.append(CareerMatchResult(
                career_id=career.id,
                slug=career.slug,
                name=career.name,
                match_pct=item["match_pct"],
                plain_reason=item["reason"],
                suits_who=career.suits_who,
                demand_level=career.demand_level,
                entry_titles=career.entry_titles or []
            ))

    # Save to DiscoveryResponse table
    disc_rec = DiscoveryResponse(
        user_id=current_user.id,
        answers=submit_req.answers,
        aptitude_scores=eval_result["aptitude_scores"],
        top_careers=[c.model_dump() for c in top_career_results]
    )
    db.add(disc_rec)

    # Log Explainable AI handoff
    top_career_name = top_career_results[0].name if top_career_results else "Career"
    log = AgentLog(
        user_id=current_user.id,
        agent_name="Discovery Agent",
        action="Evaluated Discovery Assessment",
        reason=f"Matched top 5 careers based on interests and aptitude. Highest recommendation: {top_career_name}.",
        details={"top_match": top_career_name, "aptitude": eval_result["aptitude_scores"]}
    )
    db.add(log)
    db.commit()

    return DiscoveryResultResponse(
        top_careers=top_career_results,
        aptitude_scores=eval_result["aptitude_scores"],
        summary_message=eval_result["summary_message"]
    )

@router.get("/results", response_model=DiscoveryResultResponse)
def get_discovery_results(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    latest = db.query(DiscoveryResponse).filter(
        DiscoveryResponse.user_id == current_user.id
    ).order_by(DiscoveryResponse.created_at.desc()).first()

    if not latest or not latest.top_careers:
        # Default fallback for demo purposes
        profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
        eval_result = discovery_agent.evaluate_answers({}, student_branch=profile.branch if profile else "")
        top_career_results = []
        for item in eval_result["top_careers"]:
            career = db.query(Career).filter(Career.slug == item["slug"]).first()
            if career:
                top_career_results.append(CareerMatchResult(
                    career_id=career.id,
                    slug=career.slug,
                    name=career.name,
                    match_pct=item["match_pct"],
                    plain_reason=item["reason"],
                    suits_who=career.suits_who,
                    demand_level=career.demand_level,
                    entry_titles=career.entry_titles or []
                ))
        return DiscoveryResultResponse(
            top_careers=top_career_results,
            aptitude_scores=eval_result["aptitude_scores"],
            summary_message=eval_result["summary_message"]
        )

    return DiscoveryResultResponse(
        top_careers=[CareerMatchResult(**c) for c in latest.top_careers],
        aptitude_scores=latest.aptitude_scores or {},
        summary_message="Your saved career discovery results."
    )

