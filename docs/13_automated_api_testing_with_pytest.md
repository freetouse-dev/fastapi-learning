# 13. Automated API Testing with `pytest` & `TestClient`

A quick reference and revision guide for testing FastAPI applications automatically using `pytest` and `TestClient`.

---

## 1. What Did We Do?
We introduced automated testing into our project:
1. Added `pytest` and `httpx` to our development dependencies using `uv add --dev`.
2. Created a `tests/` directory with `test_health.py` and `test_tasks.py`.
3. Used FastAPI's built-in `TestClient` to test endpoints and response payloads.
4. Ran our test suite using `uv run pytest -v`.

---

## 2. Why Did We Do It?
- **Speed**: `TestClient` uses ASGI transport in-memory. It does **not** bind to network sockets or spin up a web server, executing dozens of tests in milliseconds.
- **Regression Prevention**: As the application grows, automated tests guarantee that new features don't break existing functionality.
- **Clean Dependency Separation**: Using `uv add --dev` ensures testing packages are omitted from production Docker builds and deployments.

---

## 3. How Does It Work?

```
pytest command executed
         │
         ▼
Discovers tests/test_*.py
         │
         ▼
Runs test_*() functions
         │
         ▼
TestClient simulates HTTP requests directly through FastAPI
         │
         ▼
Validates responses using Python asserts
```

### Test Anatomy:
```python
from fastapi.testclient import TestClient
from src.taskflow_api.main import app

# 1. Initialize TestClient with the FastAPI app instance
client = TestClient(app)

def test_create_task():
    # 2. Simulate HTTP POST with JSON body
    response = client.post("/tasks/", json={"title": "Write tests", "status": "pending"})
    
    # 3. Assert HTTP status code
    assert response.status_code == 201
    
    # 4. Assert response payload
    data = response.json()
    assert data["title"] == "Write tests"
    assert "id" in data
```

---

## 4. Useful `pytest` Commands

| Command | What It Does |
| :--- | :--- |
| `uv run pytest` | Runs all discovered tests. |
| `uv run pytest -v` | Verbose mode: lists each test function name and pass/fail status. |
| `uv run pytest tests/test_tasks.py` | Runs only tests within a specific file. |
| `uv run pytest -k "health"` | Runs only tests matching the keyword `"health"`. |
| `uv run pytest -s` | Disables output capture (allows `print()` statements to display). |
