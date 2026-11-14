import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.app.config import settings
import backend.app.database as app_db
from backend.app.database import Base, get_db
from backend.app.seed.seed_runner import seed_database
from backend.app.main import app
from backend.app.utils.security import create_access_token

# Create temporary isolated SQLite test database
temp_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
TEST_DB_PATH = temp_db_file.name
temp_db_file.close()

TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override database settings and module references so app and tests use the temporary DB
settings.DATABASE_URL = TEST_DATABASE_URL
app_db.engine = test_engine
app_db.SessionLocal = TestingSessionLocal

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Initialize tables and seed fresh test database
Base.metadata.create_all(bind=test_engine)
seed_database(target_engine=test_engine, target_sessionmaker=TestingSessionLocal)

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_test_db():
    yield
    # Cleanup after test session finishes
    app.dependency_overrides.clear()
    test_engine.dispose()
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except Exception:
            pass

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def arif_token():
    return create_access_token({"user_id": 1, "email": "arif@skillpath.dev", "role": "learner"})

@pytest.fixture(scope="session")
def admin_token():
    return create_access_token({"user_id": 5, "email": "admin@skillpath.dev", "role": "admin"})

@pytest.fixture(scope="session")
def auth_headers(arif_token):
    return {"Authorization": f"Bearer {arif_token}"}

@pytest.fixture(scope="session")
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
