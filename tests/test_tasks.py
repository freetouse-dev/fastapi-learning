from fastapi.testclient import TestClient

def test_list_tasks_unauthenticated(client: TestClient):
    """Calling /tasks/ without a token must return 401 Unauthorized."""
    response = client.get("/tasks/")
    assert response.status_code == 401

def test_create_and_list_task_authenticated(client: TestClient, auth_headers: dict):
    """Creating and listing tasks with a valid token succeeds."""
    # 1. Create a task
    payload = {"title": "Write authenticated tests", "status": "pending"}
    create_res = client.post("/tasks/", json=payload, headers=auth_headers)
    assert create_res.status_code == 201
    task_data = create_res.json()
    assert task_data["title"] == "Write authenticated tests"
    assert "id" in task_data

    # 2. List tasks (must return the created task)
    list_res = client.get("/tasks/", headers=auth_headers)
    assert list_res.status_code == 200
    tasks = list_res.json()
    assert any(t["id"] == task_data["id"] for t in tasks)

def test_user_cannot_access_other_users_task(client: TestClient, auth_headers: dict):
    """User B cannot access or modify a task owned by User A (403 Forbidden)."""
    # User A creates a task
    create_res = client.post(
        "/tasks/",
        json={"title": "Alice's Secret Task", "status": "pending"},
        headers=auth_headers,
    )
    task_id = create_res.json()["id"]

    # Now create a second user (User B)
    client.post("/auth/register", json={"email": "user_b@example.com", "password": "password123"})
    login_b = client.post("/auth/login", data={"username": "user_b@example.com", "password": "password123"})
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

    # User B tries to read User A's task -> 403 Forbidden!
    get_res = client.get(f"/tasks/{task_id}", headers=headers_b)
    assert get_res.status_code == 403