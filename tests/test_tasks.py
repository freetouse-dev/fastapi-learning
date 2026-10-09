from fastapi.testclient import TestClient

from src.taskflow_api.main import app

client = TestClient(app)

def test_list_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10

def test_create_task():
    new_task_payload = {
        "title": "Write automated test cases",
        "status": "pending",
    }
    response = client.post("/tasks/", json=new_task_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write automated test cases"
    assert data["status"] == "pending"
    assert "id" in data

def test_task_not_found():
    response = client.get("/tasks/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["error_code"] == "TASK_NOT_FOUND"