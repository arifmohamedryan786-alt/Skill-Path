import pytest
from backend.app.agents.simulation_agent import simulation_agent
from backend.app.database import SessionLocal

def test_simulator_math_deterministic():
    db = SessionLocal()
    try:
        # Forecast calculation for user 1
        forecast = simulation_agent.calculate_forecast(
            db=db,
            user_id=1,
            weekly_hours_override=15.0
        )
        assert "realistic_date" in forecast
        assert "optimistic_date" in forecast
        assert "weeks_needed" in forecast
        assert forecast["weeks_needed"] > 0
        assert "total_gap_hours" in forecast
        assert "explanation" in forecast
    finally:
        db.close()

def test_get_forecast_api(client, auth_headers):
    response = client.get("/simulator/forecast", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "optimistic_date" in data
    assert "realistic_date" in data
    assert "total_gap_hours" in data
    assert "learner_pace_factor" in data

def test_run_what_if_scenario_api(client, auth_headers):
    # Test increasing weekly hours from 10 to 25
    scenario_payload = {
        "weekly_hours": 25,
        "target_career": "AI/ML Engineer"
    }
    response = client.post("/simulator/scenario", json=scenario_payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "weeks_needed" in data
    assert "optimistic_date" in data
    assert "explanation" in data
