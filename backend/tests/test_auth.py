import pytest
import uuid
from backend.app.utils.security import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hashing():
    raw_pass = "securePassword123!"
    hashed = hash_password(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("wrongPassword", hashed) is False

def test_jwt_token_cycle():
    payload = {"user_id": 99, "email": "tester@skillpath.dev", "role": "learner"}
    token = create_access_token(payload)
    assert isinstance(token, str)
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["user_id"] == 99
    assert decoded["email"] == "tester@skillpath.dev"

def test_login_demo_user(client):
    response = client.post("/auth/login", json={
        "email": "arif@skillpath.dev",
        "password": "arif123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "learner"
    assert data["user_id"] == 1

def test_login_invalid_password(client):
    response = client.post("/auth/login", json={
        "email": "arif@skillpath.dev",
        "password": "incorrect_password"
    })
    assert response.status_code == 401

def test_register_new_learner(client):
    unique_email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    response = client.post("/auth/register", json={
        "email": unique_email,
        "password": "password123",
        "full_name": "Test Student",
        "role": "learner"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user_id" in data
    assert data["full_name"] == "Test Student"

def test_guest_auth(client):
    response = client.post("/auth/guest")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "learner"
    assert "guest_" in data["email"]
    assert data["is_guest"] is True

def test_demo_auth_endpoints(client):
    for persona in ["arif", "priya", "rohan", "ananya", "admin"]:
        response = client.post(f"/auth/demo/{persona}")
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert persona in data["email"].lower()

def test_admin_learners_excludes_guest_data(client, admin_headers):
    # Create guest user
    client.post("/auth/guest")
    # Fetch admin learners
    res = client.get("/admin/learners", headers=admin_headers)
    assert res.status_code == 200
    learners = res.json()
    # Ensure no guest user appears in admin learners
    guest_emails = [l["email"] for l in learners if "guest_" in l["email"]]
    assert len(guest_emails) == 0
