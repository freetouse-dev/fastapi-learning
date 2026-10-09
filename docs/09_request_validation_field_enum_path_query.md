# 09. Request Validation with `Enum`, `Field`, `Path`, and `Query`

A quick reference and revision guide for enforcing data integrity using Python `Enum` and FastAPI/Pydantic validation tools.

---

## 1. What Did We Do?
We added strict input validation constraints:
1. Created a `TaskStatus(str, Enum)` with allowed values: `PENDING`, `IN_PROGRESS`, `COMPLETED`.
2. Added `Field(..., min_length=4, max_length=100)` to the task title.
3. Added `Path(..., ge=0)` to constrain URL task IDs.
4. Added `Query(default=10, ge=1, le=100)` to constrain pagination limits.

---

## 2. Why Did We Do It?
- **Fail Fast & Protect the Server**: Bad data is stopped right at the API boundary before running database queries or business logic.
- **Enums as Contracts**: Eliminates typos like `"complete"` vs `"completed"` and turns text inputs into clean dropdown selections in Swagger UI (`/docs`).
- **Defensive Limits**: Restricting `limit` to `1..100` prevents malicious or accidental requests from pulling millions of rows and exhausting server memory.

---

## 3. How Does It Work?

### A. Python String Enums (`str, Enum`):
```python
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
```
- Inheriting from `str` ensures seamless JSON serialization without custom encoder functions.
- FastAPI automatically validates incoming values and restricts choices in Swagger UI.

### B. Pydantic `Field`:
```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=4, max_length=100, description="Title of the task")
    status: TaskStatus = TaskStatus.PENDING
```
- `...` (Ellipsis) marks the field as strictly required.
- `min_length` and `max_length` prevent empty or excessively large strings.

### C. FastAPI `Path` and `Query`:
```python
from fastapi import Path, Query

task_id: int = Path(..., ge=0, description="Task ID must be non-negative")
limit: int = Query(default=10, ge=1, le=100, description="Limit between 1 and 100")
```

---

## 4. Common Validation Parameters Reference

| Constraint | Meaning | Used For |
| :--- | :--- | :--- |
| `gt` | Greater than | Numbers (`int`, `float`) |
| `ge` | Greater than or equal to | Numbers (`int`, `float`) |
| `lt` | Less than | Numbers (`int`, `float`) |
| `le` | Less than or equal to | Numbers (`int`, `float`) |
| `min_length` | Minimum string length | Strings |
| `max_length` | Maximum string length | Strings |
| `pattern` (regex) | Must match regular expression | Strings (emails, phone numbers, codes) |
| `description` | Explanatory note displayed in Swagger docs | Any parameter |
