# 05. Query Parameters — Filtering & Pagination

A quick reference and revision guide for handling query parameters, filtering datasets, and basic pagination in FastAPI.

---

## 1. What Did We Do?
We created a collection endpoint:
`GET /tasks?status=...&limit=...`
allowing clients to filter tasks by status and restrict the maximum number of items returned.

---

## 2. Why Did We Do It?
- **Avoid Over-Fetching**: In real applications, returning entire database tables consumes unnecessary memory and network bandwidth.
- **Client Flexibility**: Allows the frontend to request specifically what it needs (e.g. only `"completed"` tasks) without having to download and filter all items in the browser.
- **Resource Protection**: Using a `limit` with a default value prevents denial-of-service from massive query results.

---

## 3. How Does It Work?

### How FastAPI Identifies Parameter Types:
FastAPI has a clean, automatic rule:
1. If the parameter name exists in the path `{...}` $\rightarrow$ **Path Parameter** (`/tasks/{task_id}`)
2. If the parameter is a singular type (`str`, `int`, `bool`, `float`) and **not** in the path $\rightarrow$ **Query Parameter** (`/tasks?status=completed&limit=10`)

```python
@app.get("/tasks")
def list_tasks(status: str | None = None, limit: int = 10):
    ...
```

### Parameter Breakdown:
- **`status: str | None = None`**:
  - `str | None`: The parameter can be a string or `None` (Python 3.10+ union syntax).
  - `= None`: Makes the query parameter **optional**. If omitted from the URL, `status` will be `None`.
- **`limit: int = 10`**:
  - `int`: FastAPI validates that the incoming query string is convertible to an integer. If not, it returns `422 Unprocessable Entity`.
  - `= 10`: Default value when the client does not specify `?limit=...`.

---

## 4. Query URL Examples

| URL | What happens |
| :--- | :--- |
| `GET /tasks` | `status=None`, `limit=10`. Returns the first 10 tasks. |
| `GET /tasks?status=completed` | Filters tasks where `status == "completed"`, returns up to 10. |
| `GET /tasks?limit=5` | Returns the first 5 tasks of any status. |
| `GET /tasks?status=in_progress&limit=2` | Combines both filters: returns up to 2 tasks that are in progress. |
| `GET /tasks?limit=abc` | Rejected by FastAPI with `422 Unprocessable Entity`. |
