import pytest
from backend.app.utils.hashing import compute_verification_hash, verify_skill_hash

def test_passport_sha256_cryptographic_verification():
    user_id = 1
    skill_slug = "python-basics"
    score_pct = 84.5
    date_str = "2026-11-14"

    genuine_hash = compute_verification_hash(user_id, skill_slug, score_pct, date_str)
    assert isinstance(genuine_hash, str)
    assert len(genuine_hash) == 64  # SHA-256 hex string

    # 1. Genuine record passes verification
    is_valid = verify_skill_hash(genuine_hash, user_id, skill_slug, score_pct, date_str)
    assert is_valid is True

    # 2. Tampered score fails verification
    tampered_score = 99.0
    is_tampered_valid = verify_skill_hash(genuine_hash, user_id, skill_slug, tampered_score, date_str)
    assert is_tampered_valid is False

    # 3. Tampered date fails verification
    is_date_tampered = verify_skill_hash(genuine_hash, user_id, skill_slug, score_pct, "2025-01-01")
    assert is_date_tampered is False

def test_get_passport_api(client, auth_headers):
    response = client.get("/passport", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "slug" in data
    assert "verified_skills" in data
    assert "readiness_pct" in data

def test_public_passport_accessible_without_auth(client):
    # Public passport for Arif (user 1, slug arif-mohamed-0001)
    response = client.get("/passport/public/arif-mohamed-0001")
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Arif Mohamed"
    assert "verified_skills" in data
