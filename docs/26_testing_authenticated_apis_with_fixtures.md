# 26. Testing Authenticated APIs with Pytest Fixtures (`conftest.py`)

A quick reference and revision guide for testing security, authentication, and authorization using Pytest fixtures.

---

## 1. What Did We Do?
We upgraded our test suite to verify all authentication and authorization rules:
1. Created `tests/conftest.py` with two reusable fixtures:
   - `client`: session-scoped `TestClient(app)`.
   - `auth_headers`: automatically registers a unique test user, logs in to obtain a JWT token, and returns `{"Authorization": f"Bearer {token}"}`.
2. Updated `tests/test_tasks.py` with 3 core security tests:
   - `test_list_tasks_unauthenticated`: verifies requests without tokens are rejected with **`401 Unauthorized`**.
   - `test_create_and_list_task_authenticated`: verifies valid users can create (`201`) and retrieve (`200`) their tasks.
   - `test_user_cannot_access_other_users_task`: verifies that User B cannot view or modify User A's task (**`403 Forbidden`**).
3. Ran `uv run pytest -v` with 100% green tests passing.

---

## 2. Why Did We Do It?
- **Zero Test Boilerplate**: Reusable fixtures eliminate having to manually write user registration and login logic inside every test function.
- **Security Verification**: Automated tests ensure authentication (`401`) and multi-tenant authorization (`403`) policies are actively enforced on every commit.
- **Independence**: Using dynamic timestamps in emails (`test_<timestamp>@example.com`) ensures tests can run repeatedly without colliding with existing database records.

---

## 3. How Does It Work?

```
pytest discovers test_create_and_list_task_authenticated(client, auth_headers)
                                      │
                                      ▼
                 Pytest executes auth_headers from conftest.py:
                   1. POST /auth/register ➔ creates unique user
                   2. POST /auth/login    ➔ receives JWT access_token
                   3. Returns {"Authorization": f"Bearer {token}"}
                                      │
                                      ▼
                     auth_headers injected into test function:
         client.post("/tasks/", json=payload, headers=auth_headers)
                                      │
                                      ▼
                           Asserts status_code == 201
```

### Key Fixture Pattern (`conftest.py`):
```python
import pytest
from fastapi.testclient import TestClient
from src.taskflow_api.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client: TestClient):
    import time
    email = f"test_{int(time.time() * 1000)}@example.com"
    password = "testpassword123"

    client.post("/auth/register", json={"email": email, "password": password})
    login_res = client.post("/auth/login", data={"username": email, "password": password})
    token = login_res.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
```

---

## 4. Running the Tests

```bash
uv run pytest -v
```

### Result:
```
tests/test_health.py::test_health_check PASSED                           [ 25%]
tests/test_tasks.py::test_list_tasks_unauthenticated PASSED              [ 50%]
tests/test_tasks.py::test_create_and_list_task_authenticated PASSED      [ 75%]
tests/test_tasks.py::test_user_cannot_access_other_users_task PASSED     [100%]
========================= 4 passed in 8.35s =========================
```
