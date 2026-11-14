import pytest
import asyncio
from backend.app.agents.ai_mentor_agent import ai_mentor_agent
from backend.app.models.practice import PracticeQuestion, PracticeProgress

def test_get_practice_categories(client, auth_headers):
    response = client.get("/practice/categories", headers=auth_headers)
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert len(categories) == 5

    cat_slugs = [c["slug"] for c in categories]
    assert "c-programming" in cat_slugs
    assert "python" in cat_slugs
    assert "java" in cat_slugs
    assert "data-structures" in cat_slugs
    assert "dsa" in cat_slugs

    for c in categories:
        assert c["total_questions"] >= 10
        assert "description" in c
        assert "icon" in c
        assert c["beginner_count"] > 0

def test_get_practice_questions_and_filters(client, auth_headers):
    # 1. Fetch all questions
    res_all = client.get("/practice/questions", headers=auth_headers)
    assert res_all.status_code == 200
    all_qs = res_all.json()
    assert len(all_qs) >= 50

    # 2. Filter by Category = python
    res_py = client.get("/practice/questions?category=python", headers=auth_headers)
    assert res_py.status_code == 200
    py_qs = res_py.json()
    assert len(py_qs) == 10
    for q in py_qs:
        assert q["category_slug"] == "python"

    # 3. Filter by Difficulty = Beginner
    res_beg = client.get("/practice/questions?difficulty=Beginner", headers=auth_headers)
    assert res_beg.status_code == 200
    beg_qs = res_beg.json()
    assert len(beg_qs) > 0
    for q in beg_qs:
        assert q["difficulty"] == "Beginner"

    # 4. Combined Filter: category=dsa & difficulty=Intermediate
    res_dsa_inter = client.get("/practice/questions?category=dsa&difficulty=Intermediate", headers=auth_headers)
    assert res_dsa_inter.status_code == 200
    dsa_inter_qs = res_dsa_inter.json()
    assert len(dsa_inter_qs) > 0
    for q in dsa_inter_qs:
        assert q["category_slug"] == "dsa"
        assert q["difficulty"] == "Intermediate"

def test_get_question_detail_and_solution_gating(client, auth_headers):
    # Fetch first question
    res_list = client.get("/practice/questions?category=python", headers=auth_headers)
    q_id = res_list.json()[0]["id"]

    res_detail = client.get(f"/practice/questions/{q_id}", headers=auth_headers)
    assert res_detail.status_code == 200
    data = res_detail.json()

    assert data["id"] == q_id
    assert "title" in data
    assert "description" in data
    assert "hint" in data
    assert "solution" in data
    assert "explanation" in data
    assert "approach" in data
    assert "time_complexity" in data
    assert "space_complexity" in data
    assert "starter_code" in data
    assert "user_solution_code" in data

def test_practice_workspace_save_code_and_complete(client, auth_headers):
    # Pick a question
    res_list = client.get("/practice/questions?category=c-programming", headers=auth_headers)
    q_id = res_list.json()[0]["id"]

    # 1. Save workspace draft code
    sample_code = "#include <stdio.h>\n// Test solution draft"
    save_res = client.post(
        f"/practice/questions/{q_id}/progress",
        json={"status": "attempted", "solution_code": sample_code},
        headers=auth_headers
    )
    assert save_res.status_code == 200
    assert save_res.json()["user_status"] == "attempted"

    # Verify saved draft appears in detail
    check_detail = client.get(f"/practice/questions/{q_id}", headers=auth_headers).json()
    assert check_detail["user_solution_code"] == sample_code
    assert check_detail["user_status"] == "attempted"

    # 2. Mark as completed
    complete_res = client.post(
        f"/practice/questions/{q_id}/progress",
        json={"status": "completed", "solution_code": sample_code},
        headers=auth_headers
    )
    assert complete_res.status_code == 200
    assert complete_res.json()["user_status"] == "completed"

    # Verify status updated
    final_detail = client.get(f"/practice/questions/{q_id}", headers=auth_headers).json()
    assert final_detail["user_status"] == "completed"
    assert final_detail["completed_at"] is not None

def test_get_practice_stats(client, auth_headers):
    res = client.get("/practice/stats", headers=auth_headers)
    assert res.status_code == 200
    stats = res.json()

    assert "total_completed" in stats
    assert "total_attempted" in stats
    assert "total_questions" in stats
    assert stats["total_questions"] >= 50
    assert "by_category" in stats
    assert "Python" in stats["by_category"]
    assert "DSA" in stats["by_category"]
    assert "by_difficulty" in stats
    assert "Beginner" in stats["by_difficulty"]
    assert "current_streak" in stats

def test_ai_mentor_incorporates_practice_progress(db_session):
    user_id = 1  # Arif Mohamed

    # 1. Check learner context
    context = ai_mentor_agent.build_learner_context(db_session, user_id)
    assert "practice_completed" in context
    assert "practice_attempted" in context
    assert "practice_guidance" in context
    assert len(context["practice_guidance"]) > 10

    # 2. Test mentor response when asking about practice
    def _run():
        return asyncio.run(
            ai_mentor_agent.generate_response(
                db=db_session,
                user_id=user_id,
                user_message="How is my coding practice going?"
            )
        )

    response = _run()
    assert "content" in response
    assert response["tool_executed"] == "get_practice_guidance"
    # Grounded in user's real stats
    assert "Questions Completed" in response["content"] or "Problems Completed" in response["content"]
    assert "Mentor" in response["content"] or "recommendation" in response["content"].lower()

