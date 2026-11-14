import pytest

def test_get_roadmap_stages(client, auth_headers):
    response = client.get("/roadmap", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "stages" in data
    assert len(data["stages"]) == 7
    # Verify stages in order: 1 Explore -> 7 Growth
    stage_numbers = [s["stage_number"] for s in data["stages"]]
    assert stage_numbers == [1, 2, 3, 4, 5, 6, 7]

def test_get_first_week_plan(client, auth_headers):
    response = client.get("/roadmap/first-week", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert len(data["tasks"]) >= 4
    first_task = data["tasks"][0]
    assert "day" in first_task
    assert "title" in first_task
    assert "duration_mins" in first_task
    assert 20 <= first_task["duration_mins"] <= 90

def test_update_roadmap_item_status(client, auth_headers):
    # Fetch first available roadmap item
    roadmap_res = client.get("/roadmap", headers=auth_headers)
    stages = roadmap_res.json()["stages"]
    first_item = None
    for stage in stages:
        if stage.get("items") and len(stage["items"]) > 0:
            first_item = stage["items"][0]
            break

    if first_item:
        item_id = first_item["id"]
        update_res = client.put(f"/roadmap/{item_id}/status", json={"status": "completed"}, headers=auth_headers)
        assert update_res.status_code == 200
        assert update_res.json()["status"] == "completed"
