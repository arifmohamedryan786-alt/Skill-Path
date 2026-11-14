import pytest
from backend.app.agents.orchestrator import AgentOrchestrator
from backend.app.database import SessionLocal
from backend.app.models.agent_log import AgentLog

def test_orchestrator_logs_action():
    db = SessionLocal()
    try:
        orchestrator = AgentOrchestrator()
        result = orchestrator.on_inactivity_detected(db, user_id=1)
        assert result["status"] == "rebalanced"

        # Check that log was written to database
        recent_log = db.query(AgentLog).filter(
            AgentLog.agent_name == "Orchestrator",
            AgentLog.action == "Inactivity Rebalance"
        ).order_by(AgentLog.id.desc()).first()

        assert recent_log is not None
        assert "7 days of inactivity" in recent_log.reason
    finally:
        db.close()

def test_get_agent_logs_api(client, auth_headers):
    response = client.get("/agents/logs", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        first_log = data[0]
        assert "agent_name" in first_log
        assert "action" in first_log
