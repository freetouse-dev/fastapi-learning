# 02. First FastAPI Endpoint & ASGI Server (Uvicorn)

A quick reference and revision guide for creating your first FastAPI application and running it with Uvicorn.

---

## 1. What Did We Do?
We created `src/taskflow_api/main.py`, instantiated the `FastAPI` application, and defined our first route: a health-check endpoint (`GET /health`).

---

## 2. Why Did We Do It?
- **Application Instance (`FastAPI()`)**: The central registry where all routes, middlewares, event handlers, and dependencies live.
- **Health Check Endpoint (`/health`)**: An industry-standard endpoint used by monitoring systems, load balancers, and cloud platforms (AWS/Kubernetes) to verify that the service is running and ready to handle traffic.

---

## 3. How Does It Work?

```python
from fastapi import FastAPI

# 1. Create the application instance
app = FastAPI(title="TaskFlow API", version="0.1.0")

# 2. Register a route with the path operation decorator
@app.get("/health")
def health_check():
    # 3. Return Python native data; FastAPI serializes to JSON automatically
    return {"status": "ok", "message": "TaskFlow API is running"}
```

### Key Components:
1. **Path Operation Decorator**: `@app.get("/health")`
   - Method: HTTP `GET`
   - Path: `/health`
2. **Path Operation Function**: `def health_check():`
   - Regular `def` vs `async def`:
     - Use `def` for standard synchronous operations (FastAPI automatically runs it in an external threadpool so it doesn't block the main event loop).
     - Use `async def` when performing non-blocking async I/O (e.g. `await db.execute(...)`).
3. **Automatic JSON Serialization**:
   - Dictionaries and lists returned from the function are automatically converted into JSON with `Content-Type: application/json` and status code `200 OK`.
4. **Auto-Generated Documentation**:
   - Swagger UI: `http://127.0.0.1:8000/docs` (interactive API explorer)
   - ReDoc: `http://127.0.0.1:8000/redoc` (clean reference documentation)

---

## 4. Running the Server with `uv`

```bash
uv run uvicorn taskflow_api.main:app --reload
```

| Part | Meaning |
| :--- | :--- |
| `uv run` | Executes using the project's virtual environment. |
| `uvicorn` | High-performance ASGI web server. |
| `taskflow_api.main` | Module path pointing to `src/taskflow_api/main.py`. |
| `:app` | Variable name of the `FastAPI()` instance. |
| `--reload` | Watches files and reloads the server automatically on code changes. |
