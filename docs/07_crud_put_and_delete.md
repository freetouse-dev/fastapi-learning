# 07. Completing CRUD — `PUT` (Update) and `DELETE` (Remove)

A quick reference and revision guide for completing the full CRUD lifecycle with HTTP `PUT` and `DELETE`.

---

## 1. What Did We Do?
We implemented:
- `PUT /tasks/{task_id}`: Updates an existing task by ID using data from the JSON request body.
- `DELETE /tasks/{task_id}`: Deletes an existing task by ID and returns HTTP status code `204 No Content`.

With this, our API now supports all 4 standard CRUD operations:
- **C**reate: `POST /tasks` (`201 Created`)
- **R**ead: `GET /tasks` & `GET /tasks/{id}` (`200 OK`)
- **U**pdate: `PUT /tasks/{id}` (`200 OK`)
- **D**elete: `DELETE /tasks/{id}` (`204 No Content`)

---

## 2. Why Did We Do It?
- **Combining Path & Body Parameters**: Real-world update endpoints must identify *which* record to change via URL path (`{task_id}`) while delivering *what* changed via request body (`task_data: TaskCreate`).
- **Standardizing HTTP Deletion**: Returning `204 No Content` communicates to clients that the resource was removed and no payload needs to be parsed.

---

## 3. How Does It Work?

### A. Updating with `PUT`:
```python
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskCreate):
    for task in TASKS:
        if task["id"] == task_id:
            task["title"] = task_data.title
            task["status"] = task_data.status
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )
```
- FastAPI simultaneously parses `task_id` from the URL path and validates `task_data` against the `TaskCreate` Pydantic schema.
- If no matching task is found, it raises `404 Not Found`.

### B. Deleting with `DELETE` & `204 No Content`:
```python
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(TASKS):
        if task["id"] == task_id:
            TASKS.pop(index)
            return  # Empty return for 204
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )
```
- When `status_code=status.HTTP_204_NO_CONTENT` is set, returning `None` sends an HTTP response with zero body bytes and a status of `204`.

---

## 4. REST Method & Status Code Summary

| Operation | HTTP Method | Endpoint | Success Status Code | Typical Response Body |
| :--- | :--- | :--- | :--- | :--- |
| Create | `POST` | `/tasks` | `201 Created` | Newly created task JSON |
| Read All | `GET` | `/tasks` | `200 OK` | Array of tasks `[...]` |
| Read One | `GET` | `/tasks/{id}` | `200 OK` | Single task JSON `{...}` |
| Update | `PUT` | `/tasks/{id}` | `200 OK` | Updated task JSON `{...}` |
| Delete | `DELETE` | `/tasks/{id}` | `204 No Content` | *(Empty)* |
