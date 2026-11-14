import pytest

def test_generate_assessment_endpoint(client, auth_headers):
    response = client.get("/assessments/generate?skill_slug=python-basics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) >= 3
    assert "target_level" in data
    assert "practical_task" in data

def test_submit_passing_assessment(client, auth_headers):
    # Fetch assessment first
    gen_res = client.get("/assessments/generate?skill_slug=python-basics", headers=auth_headers)
    a_data = gen_res.json()
    a_id = a_data["id"]

    # Submit passing answers (questions 1..5, correct_index is typically 0)
    passing_submission = {
        "assessment_id": a_id,
        "mcq_answers": {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        },
        "practical_code": "def solve():\n    return 'passed test'"
    }
    response = client.post("/assessments/submit", json=passing_submission, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert "score_pct" in result
    assert "passed" in result
    assert result["score_pct"] >= 70
    assert result["passed"] is True
    assert result["verification_hash"] is not None

def test_submit_failing_assessment_triggers_remedial(client, auth_headers):
    gen_res = client.get("/assessments/generate?skill_slug=python-basics", headers=auth_headers)
    a_data = gen_res.json()
    a_id = a_data["id"]

    # Submit deliberately wrong answers (index 3 or 9)
    failing_submission = {
        "assessment_id": a_id,
        "mcq_answers": {
            1: 3,
            2: 3,
            3: 3,
            4: 3,
            5: 3
        },
        "practical_code": ""
    }
    response = client.post("/assessments/submit", json=failing_submission, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["passed"] is False
    assert result["score_pct"] < 70
    assert "remedial_topics" in result
    assert len(result["remedial_topics"]) > 0
