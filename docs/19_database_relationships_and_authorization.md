# 19. Database Relationships & Resource Authorization (`403 Forbidden`)

A quick reference and revision guide for relational foreign keys, task ownership, and multi-tenant resource authorization in FastAPI.

---

## 1. What Did We Do?
We connected the `User` and `Task` entities with relational database constraints and enforced resource ownership:
1. Added `owner_id = mapped_column(Integer, ForeignKey("users.id"))` to `Task`.
2. Created a bidirectional SQLAlchemy relationship:
   - `Task.owner = relationship("User", back_populates="tasks")`
   - `User.tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")`
3. Updated `TaskResponse` to include `owner_id: int`.
4. Enforced authentication across all `/tasks` routes using `current_user: User = Depends(get_current_user)`.
5. Enforced ownership authorization:
   - `GET /tasks/`: automatically filters by `Task.owner_id == current_user.id`.
   - `POST /tasks/`: automatically stamps `owner_id = current_user.id`.
   - `GET /tasks/{id}`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`: rejects access with **`403 Forbidden`** if `task.owner_id != current_user.id`.

---

## 2. Why Did We Do It?
- **Data Isolation**: Ensures complete data privacy in multi-user applications. User A can never view, mutate, or delete User B's resources.
- **Relational Integrity**: Foreign key constraints ensure tasks cannot reference non-existent users, and `cascade="all, delete-orphan"` automatically cleans up tasks if a user account is deleted.
- **Defense in Depth**: Even if a malicious actor guesses another user's task ID (e.g., `/tasks/1`), the API blocks the request with `403 Forbidden`.

---

## 3. How Does It Work?

### A. Authentication (401) vs Authorization (403):
```
Client Request
      │
      ▼
Does request have a valid JWT token?
  ├── NO  ➔ 401 Unauthorized ("Could not validate credentials")
  └── YES ➔ User identity confirmed (e.g., User ID 2 - Bob)
      │
      ▼
Does Task exist in DB?
  ├── NO  ➔ 404 Not Found
  └── YES ➔ Task found (e.g., owned by User ID 1 - Alice)
      │
      ▼
Does task.owner_id == current_user.id?
  ├── NO  ➔ 403 Forbidden ("You don't have permission to modify this task")
  └── YES ➔ Action allowed! (200 / 201 / 204)
```

### B. SQLAlchemy Relationship Syntax:
```python
# In models/task.py
owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
owner: Mapped["User"] = relationship("User", back_populates="tasks")

# In models/user.py
tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
```
- `back_populates`: Synchronizes both sides of the relationship in Python memory.
- `cascade="all, delete-orphan"`: Automatically deletes all tasks belonging to a user if that user is deleted from the database.
