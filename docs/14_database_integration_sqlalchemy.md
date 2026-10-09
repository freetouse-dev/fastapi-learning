# 14. Database Integration with SQLAlchemy & SQLite

A quick reference and revision guide for setting up SQLAlchemy ORM, SQLite, and the database session dependency in FastAPI.

---

## 1. What Did We Do?
We integrated a real relational database using **SQLAlchemy** and **SQLite**:
1. Installed SQLAlchemy with `uv add sqlalchemy`.
2. Created `database.py` with:
   - `engine`: handles connection pooling and raw SQL execution.
   - `SessionLocal`: factory for database sessions.
   - `Base`: declarative base class for ORM models.
   - `get_db`: generator dependency managing session lifecycles.
3. Created our first ORM Model: `models/task.py` representing the `tasks` table.

---

## 2. Pydantic Schemas vs. SQLAlchemy ORM Models

| Feature | Pydantic Schemas (`schemas/task.py`) | SQLAlchemy Models (`models/task.py`) |
| :--- | :--- | :--- |
| **Layer** | **HTTP / API Layer** | **Database / Storage Layer** |
| **Responsibility** | Validates incoming JSON and serializes outgoing JSON | Defines SQL tables, columns, indexes, and relationships |
| **Inherits From** | `pydantic.BaseModel` | `sqlalchemy.orm.DeclarativeBase` |
| **Output** | Python objects / JSON dictionaries | ORM objects bound to a database session |

---

## 3. How Does the `get_db` Dependency Work?

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### The Request Lifecycle:
1. **Request arrives**: FastAPI calls `get_db()`, instantiates `db = SessionLocal()`, and pauses at `yield db`.
2. **Endpoint executes**: The route handler receives `db` and runs queries or transactions.
3. **Response returned**: FastAPI resumes `get_db()` and executes the `finally:` block.
4. **Session closes**: `db.close()` releases the database connection back to the pool, preventing memory and connection leaks.

---

## 4. SQLAlchemy 2.0 Typed Model Definition

```python
from sqlalchemy import Integer, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from taskflow_api.database import Base
from taskflow_api.schemas.task import TaskStatus

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False
    )
```

- **`Mapped[T]`**: Modern SQLAlchemy 2.0 type-hinting for IDE autocompletion and static type analysis.
- **`primary_key=True, index=True`**: Creates an indexed primary key column for fast lookups.
