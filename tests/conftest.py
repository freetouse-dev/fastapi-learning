import pytest
from fastapi.testclient import TestClient
from src.taskflow_api.main import app

@pytest.fixture(scope="session")
def client():
    """Provides a reusable FastAPI TestClient across the test session."""
    return TestClient(app)

@pytest.fixture
def auth_headers(client: TestClient):
    """Registers a unique test user, logs in, and returns Authorization headers."""
    import time
    unique_email = f"test_{int(time.time() * 1000)}@example.com"
    password = "testpassword123"

    client.post("/auth/register", json={"email": unique_email, "password": password})

    login_res = client.post("/auth/login", data={"username": unique_email, "password": password})
    token = login_res.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}