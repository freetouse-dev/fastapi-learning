# 08. Response Models & Schema Separation

A quick reference and revision guide for using `response_model` and separating request schemas from response schemas in FastAPI.

---

## 1. What Did We Do?
We created a dedicated output schema:
```python
class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
```
and attached it to our routes using `response_model`:
- `response_model=TaskResponse` for single item endpoints (`GET`, `POST`, `PUT`)
- `response_model=list[TaskResponse]` for collection endpoints (`GET /tasks`)

---

## 2. Why Did We Do It?

### 1. Security & Data Protection (Preventing Data Leaks)
In production, your internal database records or objects often contain sensitive or internal attributes (e.g., `hashed_password`, `internal_id`, `stripe_customer_id`, `is_deleted`). 
With `response_model`, FastAPI **automatically filters out** any fields that are not declared in the response schema before sending the JSON to the client.

### 2. Clear Separation of Concerns
- **Input Schema (`TaskCreate`)**: Dictates what the *client sends to us*. Does **not** include an `id` because the server/database assigns the ID.
- **Output Schema (`TaskResponse`)**: Dictates what the *server sends back*. Includes the generated `id`.

### 3. Precise API Documentation
In Swagger UI (`/docs`), clients see the exact contract and types they will receive in the response body.

---

## 3. How Does It Work?

```python
# Single object response
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    ...

# List of objects response
@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(status: str | None = None, limit: int = 10):
    ...
```

### Key Behaviors:
- **Automatic Serialization**: Converts internal models, dictionaries, or ORM objects into JSON matching the schema.
- **Response Validation**: If your endpoint tries to return data that doesn't match `TaskResponse`, FastAPI raises an internal error rather than leaking invalid shapes to the client.
- **Notice on `DELETE`**: Endpoints returning `204 No Content` do not need a `response_model` because the HTTP body is intentionally empty.
