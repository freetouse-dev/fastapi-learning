# 10. Project Structure & `APIRouter` (Modular Architecture)

A quick reference and revision guide for structuring real-world FastAPI applications using `APIRouter`.

---

## 1. What Did We Do?
We refactored our monolithic `main.py` into a modular package architecture:
- Extracted Pydantic schemas into `schemas/task.py`.
- Extracted route handlers into `routers/tasks.py` and `routers/health.py` using `APIRouter`.
- Kept `main.py` minimal and focused on application assembly.

### Project Layout:
```
src/taskflow_api/
├── __init__.py
├── main.py
├── schemas/
│   ├── __init__.py
│   └── task.py
└── routers/
    ├── __init__.py
    ├── health.py
    └── tasks.py
```

---

## 2. Why Did We Do It?
- **Maintainability**: Large real-world APIs with 50+ endpoints cannot live in a single file. Modularizing by resource keeps files small, readable, and easy to maintain.
- **DRY (Don't Repeat Yourself)**: Instead of writing `/tasks` on every route decorator, the router sets a common `prefix="/tasks"`.
- **Automatic Documentation Grouping**: The `tags=["Tasks"]` argument automatically organizes endpoints into categorized sections in Swagger UI (`/docs`).
- **Team Scale**: Allows multiple developers to work on different domain routers (`users.py`, `tasks.py`, `auth.py`) without git merge conflicts.

---

## 3. How Does It Work?

### A. Creating an `APIRouter` (`routers/tasks.py`):
```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks",   # Every route in this file starts with /tasks
    tags=["Tasks"]     # Section header in /docs
)

@router.get("/")       # Matches GET /tasks/
def list_tasks(...):
    ...

@router.get("/{task_id}")  # Matches GET /tasks/{task_id}
def get_task(...):
    ...
```

### B. Registering Routers in `main.py`:
```python
from fastapi import FastAPI
from taskflow_api.routers import health, tasks

app = FastAPI(title="TaskFlow API", version="0.1.0")

# Mount routers onto the main app
app.include_router(health.router)
app.include_router(tasks.router)
```

---

## 4. Best Practices for `APIRouter`
1. **Keep routers focused on HTTP**: Routers should validate input, delegate logic, and return responses. They shouldn't contain low-level database engine configurations.
2. **Use Plural Nouns for Resource Prefixes**: Use `/tasks`, `/users`, `/projects`.
3. **Always Tag Routers**: Provide `tags=[...]` so your API documentation remains neat and easy to navigate.
