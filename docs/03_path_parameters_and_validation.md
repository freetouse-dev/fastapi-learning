# 03. Path Parameters & Automatic Data Validation

A quick reference and revision guide for path parameters and FastAPI's automatic type parsing and validation.

---

## 1. What Did We Do?
We created our first parameterized route:
`GET /tasks/{task_id}`
to fetch a specific task by its identifier.

---

## 2. Why Did We Do It?
- **Resource Identification**: In REST APIs, specific resources are accessed via unique identifiers in the URL path (e.g. `/tasks/1`, `/tasks/2`).
- **Type Safety**: URLs are plain strings. We need integers in our Python logic. FastAPI bridges this gap cleanly.

---

## 3. How Does It Work?

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    ...
```

### The 3 Superpowers of Python Type Hints in FastAPI:

1. **Automatic Type Conversion (Parsing)**:
   - When a client calls `/tasks/1`, FastAPI receives string `"1"` and converts it to Python integer `1`.

2. **Automatic Data Validation (422 Unprocessable Entity)**:
   - When a client calls `/tasks/abc`, FastAPI immediately rejects the request:
     - **Status code**: `422 Unprocessable Entity`
     - **Response body**:
       ```json
       {
         "detail": [
           {
             "type": "int_parsing",
             "loc": ["path", "task_id"],
             "msg": "Input should be a valid integer, unable to parse string as an integer",
             "input": "abc"
           }
         ]
       }
       ```
   - Your route function is never executed with invalid data, preventing crashes.

3. **Automatic OpenAPI / Swagger Documentation**:
   - In `/docs`, `task_id` is automatically declared as an `integer` path parameter with input validation and schema documentation.
