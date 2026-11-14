import pytest
from backend.app.agents.career_matcher_agent import career_matcher_agent
from backend.app.database import SessionLocal

def test_career_matcher_formula_deterministic():
    db = SessionLocal()
    try:
        # User 1 (Arif Mohamed) matched against Career 1 (Full Stack) or Career 5 (AI/ML)
        result = career_matcher_agent.calculate_match(db, user_id=1, career_id=5)
        assert "match_pct" in result
        assert "gaps" in result
        assert "strengths" in result
        assert 0.0 <= result["match_pct"] <= 100.0
        assert "readiness_label" in result
    finally:
        db.close()

def test_get_career_match_api(client, auth_headers):
    response = client.get("/match", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "career_name" in data
    assert "match_pct" in data
    assert 0 <= data["match_pct"] <= 100
    assert "gaps" in data
    assert "strengths" in data
