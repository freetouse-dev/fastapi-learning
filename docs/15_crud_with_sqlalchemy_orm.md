# 15. Connecting Routes to the Database (CRUD with SQLAlchemy)

A quick reference and revision guide for performing database CRUD operations using SQLAlchemy ORM and FastAPI.

---

## 1. What Did We Do?
We replaced our temporary in-memory `TASKS` list with persistent database operations:
1. Added `model_config = ConfigDict(from_attributes=True)` to `TaskResponse`.
2. Registered the `task` model in `main.py` so SQLite tables are automatically created on startup.
3. Injected `db: Session = Depends(get_db)` into all CRUD routes in `routers/tasks.py`.
4. Replaced list manipulations with SQLAlchemy queries, commits, and refreshes.

---

## 2. Why Did We Do It?
- **Data Persistence**: Data now lives in SQLite (`taskflow.db`) and survives server restarts and crashes.
- **ACID Transactions**: `db.commit()` ensures database writes are atomic, consistent, isolated, and durable.
- **Relational Capabilities**: Prepares the application for relations (Users, Workspaces, Comments) and indexes.

---

## 3. How Does It Work?

### A. Pydantic `from_attributes = True`
```python
class TaskResponse(BaseModel):
    id: int
    title: str
    status: TaskStatus

    model_config = ConfigDict(from_attributes=True)
```
- **Why it's required**: FastAPI routes now return SQLAlchemy ORM objects (`task.id`, `task.title`) instead of dictionaries (`task["id"]`).
- Setting `from_attributes=True` instructs Pydantic to read object attributes instead of dictionary keys when serializing responses.

### B. Table Registration in `main.py`
```python
from taskflow_api.database import Base, engine
from taskflow_api.models import task as task_model

Base.metadata.create_all(bind=engine)
```
- `Base.metadata.create_all` inspects all models registered in Python memory. Importing `task_model` guarantees the `tasks` table is detected and created.

### C. SQLAlchemy CRUD Operations Breakdown

| Operation | SQLAlchemy Code | Explanation |
| :--- | :--- | :--- |
| **Create** | `db_task = Task(...)`<br>`db.add(db_task)`<br>`db.commit()`<br>`db.refresh(db_task)` | Stages object in session, writes transaction to disk, and refreshes object with generated `id`. |
| **Read All** | `db.query(Task).offset(skip).limit(limit).all()` | Generates `SELECT * FROM tasks LIMIT ... OFFSET ...`. |
| **Read One** | `db.query(Task).filter(Task.id == id).first()` | Generates `SELECT * FROM tasks WHERE id = ? LIMIT 1`. |
| **Update** | `db_task.title = new_title`<br>`db.commit()`<br>`db.refresh(db_task)` | Modifies object attributes and commits the `UPDATE` query. |
| **Delete** | `db.delete(db_task)`<br>`db.commit()` | Marks object for deletion and commits the `DELETE` query. |
