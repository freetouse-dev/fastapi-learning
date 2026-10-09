# 12. Custom Exceptions & Global Exception Handlers

A quick reference and revision guide for domain-driven exceptions and centralized error handling in FastAPI.

---

## 1. What Did We Do?
We created a custom Python domain exception and registered a global handler on the FastAPI application:
1. Created `TaskNotFoundError` in `exceptions.py`.
2. Registered `@app.exception_handler(TaskNotFoundError)` in `main.py`.
3. Updated routes to raise `TaskNotFoundError(task_id)` instead of hardcoded `HTTPException`.

---

## 2. Why Did We Do It?

### 1. Separation of Concerns (Domain vs HTTP)
Business logic and service layers shouldn't care about HTTP details (status codes, headers, response JSON shapes). They should raise clear domain errors (e.g. `TaskNotFoundError`, `InsufficientFundsError`, `UserAlreadyExistsError`).

### 2. Standardized Error Contracts
Instead of different developers returning random dictionary shapes on errors, the global handler enforces a consistent error structure across the entire API:
```json
{
  "error_code": "TASK_NOT_FOUND",
  "detail": "Task id 99 was not found"
}
```

### 3. Cleaner Route Code
Routes are more expressive and readable:
```python
# Before:
raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")

# After:
raise TaskNotFoundError(task_id)
```

---

## 3. How Does It Work?

```
Client request for non-existent resource
                 │
                 ▼
     Route raises TaskNotFoundError(99)
                 │
                 ▼
  FastAPI intercepts the raised exception
                 │
                 ▼
Calls @app.exception_handler(TaskNotFoundError)
                 │
                 ▼
Returns standardized JSONResponse with HTTP 404
```

### Code Implementation:

#### 1. The Domain Exception (`exceptions.py`):
```python
class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
```

#### 2. The Global Handler (`main.py`):
```python
@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": "TASK_NOT_FOUND",
            "detail": f"Task id {exc.task_id} was not found",
        },
    )
```

#### 3. In the Router (`routers/tasks.py`):
```python
if task["id"] == task_id:
    return task

raise TaskNotFoundError(task_id)
```
