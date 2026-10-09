# 04. HTTP Status Codes & Raising `HTTPException`

A quick reference and revision guide for HTTP status codes and throwing errors properly in FastAPI.

---

## 1. What Did We Do?
We replaced a custom dictionary error (`return {"error": ...}`) with FastAPI's `HTTPException` and used `status.HTTP_404_NOT_FOUND`.

---

## 2. Why Did We Do It?
- **Avoid the 200 OK Anti-Pattern**: In REST APIs, returning an HTTP `200 OK` status with a body containing `"error": "..."` confuses frontend clients and automated tools, which look at HTTP status headers to determine success or failure.
- **Consistent Error Structure**: Raising `HTTPException` ensures all errors follow a standard JSON response shape: `{"detail": "..."}`.
- **Clean Execution Flow**: `raise` immediately stops further code execution within the route, preventing unwanted logic from executing.

---

## 3. How Does It Work?

```python
from fastapi import HTTPException, status

raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Task with ID {task_id} not found"
)
```

### Key Concepts:
1. **`status` module**: Provides clear, self-documenting HTTP status constants (e.g., `status.HTTP_404_NOT_FOUND`, `status.HTTP_201_CREATED`, `status.HTTP_400_BAD_REQUEST`) instead of using magic numbers like `404` or `201`.
2. **`detail` parameter**: A human-readable description of what went wrong. Can be a string, list, or dictionary.
3. **Response Headers**: `HTTPException` also accepts optional `headers` (e.g., `headers={"WWW-Authenticate": "Bearer"}` for auth errors).

---

## 4. Common HTTP Status Codes in REST APIs

| Status Code | Constant | When to Use |
| :--- | :--- | :--- |
| **`200 OK`** | `status.HTTP_200_OK` | Successful GET, PUT, or PATCH. |
| **`201 Created`** | `status.HTTP_201_CREATED` | Successful POST creating a new resource. |
| **`204 No Content`** | `status.HTTP_204_NO_CONTENT` | Successful DELETE (no response body). |
| **`400 Bad Request`** | `status.HTTP_400_BAD_REQUEST` | Client sent malformed business data. |
| **`401 Unauthorized`** | `status.HTTP_401_UNAUTHORIZED` | Missing or invalid authentication token. |
| **`403 Forbidden`** | `status.HTTP_403_FORBIDDEN` | Authenticated, but lacks permission for this resource. |
| **`404 Not Found`** | `status.HTTP_404_NOT_FOUND` | Resource does not exist. |
| **`422 Unprocessable Entity`** | `status.HTTP_422_UNPROCESSABLE_ENTITY` | Pydantic schema / type validation failed. |
| **`500 Internal Server Error`** | `status.HTTP_500_INTERNAL_SERVER_ERROR` | Unhandled server crash / exception. |
