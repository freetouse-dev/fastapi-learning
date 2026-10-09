# 06. Request Body & Pydantic Models (`POST`)

A quick reference and revision guide for accepting JSON payloads, data validation with Pydantic, and returning `201 Created`.

---

## 1. What Did We Do?
We created a `POST /tasks` endpoint that accepts incoming JSON data, validates it using a Pydantic `BaseModel` (`TaskCreate`), and returns the newly created task with status code `201 Created`.

---

## 2. Why Did We Use Pydantic?
- **Input Validation**: Automatically rejects missing required fields, bad data types, or malformed JSON with descriptive `422 Unprocessable Entity` errors.
- **Type Safety**: Developers get IDE autocomplete and guaranteed data types inside route functions.
- **Contract Enforcement**: Clearly communicates to API consumers (and frontend teams) what fields are expected and required.
- **Interactive Documentation**: Swagger UI (`/docs`) automatically generates editable sample request bodies.

---

## 3. How Does FastAPI Distinguish Parameter Types?

FastAPI uses the Python type hint and decorator path to determine where data comes from:

| Syntax in Function | Where FastAPI Looks | Example |
| :--- | :--- | :--- |
| Variable declared in path `{task_id}` | **URL Path** | `@app.get("/tasks/{task_id}")`<br>`def get_task(task_id: int):` |
| Primitive type (`str`, `int`, etc.) **not** in path | **Query String** | `def list_tasks(status: str \| None = None):` |
| Subclass of `pydantic.BaseModel` | **Request Body (JSON)** | `def create_task(task_data: TaskCreate):` |

---

## 4. Code Breakdown

```python
from pydantic import BaseModel
from fastapi import status

# 1. Define the input contract
class TaskCreate(BaseModel):
    title: str               # Required field
    status: str = "pending"  # Optional field with default value

# 2. Use the schema in a POST route with 201 Created
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    new_id = len(TASKS) + 1
    new_task = {
        "id": new_id,
        "title": task_data.title,
        "status": task_data.status,
    }
    TASKS.append(new_task)
    return new_task
```

### Key Takeaways:
- **`status_code=status.HTTP_201_CREATED`**: According to REST conventions, creating a resource should respond with `201`, not `200`.
- **Default values**: If a field has a default value (`= "pending"`), it becomes optional in the incoming JSON payload.
