# 11. Dependency Injection (`Depends`)

A quick reference and revision guide for understanding FastAPI's Dependency Injection system.

---

## 1. What Did We Do?
We created a reusable dependency function for pagination:
```python
def pagination_params(
    skip: int = Query(default=0, ge=0, description="skip should be greater than 0"),
    limit: int = Query(default=10, ge=1, le=100, description="limit should be 1-100")
):
    return {"skip": skip, "limit": limit}
```
and injected it into our route using `Depends(pagination_params)`:
```python
@router.get("/", response_model=list[TaskResponse])
def list_tasks(status: TaskStatus | None = None, pagination: dict = Depends(pagination_params)):
    ...
```

---

## 2. Why Did We Do It?
- **DRY (Don't Repeat Yourself)**: Instead of declaring `skip` and `limit` on every list endpoint in the project, we declared it once.
- **Single Source of Truth**: Changing pagination defaults, validation rules, or limits requires updating only the dependency function.
- **Separation of Concerns**: Route handlers focus on business logic rather than parsing and validating repetitive query parameters.
- **Universal Pattern**: In FastAPI, this exact pattern is used for:
  - Database sessions (`db: Session = Depends(get_db)`)
  - Authentication (`current_user: User = Depends(get_current_user)`)
  - Permission checks (`admin: User = Depends(require_admin)`)

---

## 3. How Does It Work?

```
Client Request (GET /tasks/?skip=2&limit=5)
                 │
                 ▼
       FastAPI inspects route
                 │
                 ▼
       Detects Depends(pagination_params)
                 │
                 ▼
  Executes pagination_params(skip=2, limit=5)
                 │
                 ▼
  Injects returned dict into list_tasks(pagination=...)
                 │
                 ▼
         Route handler executes
```

### Key Insights:
1. **Automatic Documentation**: FastAPI inspects the parameters inside the dependency function and automatically documents `skip` and `limit` in Swagger UI (`/docs`).
2. **Type Safety**: The return value of the dependency becomes the argument value in your route.
3. **Hierarchical Dependencies**: Dependencies can themselves depend on other dependencies (sub-dependencies).
