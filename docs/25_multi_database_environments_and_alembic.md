# 25. Multi-Database Environments & Alembic Operations

A quick reference and revision guide for managing multiple database backends (SQLite & MySQL), Alembic synchronization, and ORM relationship registration.

---

## 1. What Did We Learn?
In real-world architectures, applications often target different database backends:
- **Local Dev**: MySQL running on `localhost:3306/master`.
- **Docker Container**: Isolated SQLite database file `/app/taskflow.db`.
- **CI / Testing**: In-memory SQLite or test database.

We solved two critical database challenges:
1. Synchronizing Alembic migrations across different database instances.
2. Resolving circular SQLAlchemy ORM relationship references.

---

## 2. Alembic: `stamp` vs `upgrade`

Understanding the difference between `stamp` and `upgrade` is crucial:

| Command | What It Actually Does | When to Use |
| :--- | :--- | :--- |
| **`alembic upgrade head`** | **Executes the SQL DDL commands** (`CREATE TABLE`, `ALTER TABLE`) on the database AND marks the revision as complete. | When you want to actually create or modify tables in your database. |
| **`alembic stamp <revision>`** | **Only updates the `alembic_version` table**. Does **NOT** execute any SQL table creation scripts! | Only when tables already exist in the database and you need to tell Alembic to track them without re-creating them. |

> **Key Rule**: If you run `alembic stamp <revision>` on an empty database, Alembic thinks the tables are already there, but they were never actually created! Always run `alembic upgrade head` to execute the actual table creation scripts.

---

## 3. Resolving SQLAlchemy Relationships (`models/__init__.py`)

### The Problem:
In `models/user.py`, the `User` model defines:
```python
tasks: Mapped[list["Task"]] = relationship("Task", ...)
```
When Python imports `User` without importing `Task`, SQLAlchemy's string-based relationship mapper searches its internal registry for `'Task'`. If `Task` has not yet been loaded into Python memory, SQLAlchemy throws:
`InvalidRequestError: expression 'Task' failed to locate a name ('Task')`.

### The Solution:
Expose all ORM models together in `src/taskflow_api/models/__init__.py`:
```python
from taskflow_api.models.task import Task
from taskflow_api.models.user import User

__all__ = ["Task", "User"]
```
And import `taskflow_api.models` on application startup in `main.py`:
```python
import taskflow_api.models  # Guarantees all ORM relationships are registered
```

---

## 4. Environment Switching Summary

Thanks to `pydantic-settings`, switching database backends requires **zero code changes**:

```ini
# To use SQLite (Docker default or quick testing):
DATABASE_URL="sqlite:///./taskflow.db"

# To use MySQL (Local development):
DATABASE_URL="mysql+pymysql://user:password@localhost:3306/dbname"

# To use PostgreSQL (Production / Cloud):
DATABASE_URL="postgresql+psycopg://user:password@db.example.com:5432/dbname"
```
Alembic and SQLAlchemy automatically adapt their SQL dialects to whichever engine is declared in `DATABASE_URL`.
