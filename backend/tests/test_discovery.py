import pytest

def test_get_discovery_questions(client):
    response = client.get("/discovery/questions")
    assert response.status_code == 200
    questions = response.json()
    assert isinstance(questions, list)
    assert len(questions) >= 10
    first_q = questions[0]
    assert "id" in first_q
    assert "question" in first_q
    assert "options" in first_q

def test_submit_discovery_answers_and_get_results(client, auth_headers):
    # Submit 15 answers representing an analytical student interested in data & AI
    answers = {
        "q1": "analyze_data",
        "q2": "math_stats",
        "q3": "solving_puzzles",
        "q4": "collaborative",
        "q5": "structured",
        "q6": "python",
        "q7": "data_analysis",
        "q8": "machine_learning",
        "q9": "sql",
        "q10": "cloud_curious",
        "q11": "tech_industry",
        "q12": "btech_ai_ds",
        "q13": "pattern_recognition",
        "q14": "intermediate_coding",
        "q15": "high_motivation"
    }
    submit_res = client.post("/discovery/submit", json={"answers": answers}, headers=auth_headers)
    assert submit_res.status_code == 200

    results_res = client.get("/discovery/results", headers=auth_headers)
    assert results_res.status_code == 200
    data = results_res.json()
    assert "top_careers" in data
    assert len(data["top_careers"]) <= 5
    assert len(data["top_careers"]) >= 3

    top_career = data["top_careers"][0]
    assert "career_id" in top_career
    assert "name" in top_career
    assert "match_pct" in top_career
    assert top_career["match_pct"] > 50
    assert "plain_reason" in top_career
    assert len(top_career["plain_reason"]) > 10
