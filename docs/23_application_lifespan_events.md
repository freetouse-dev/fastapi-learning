# 23. Application Lifespan Events (`lifespan`)

A quick reference and revision guide for managing application startup and graceful shutdown in modern FastAPI.

---

## 1. What Did We Do?
We implemented a modern **Lifespan Context Manager** in `src/taskflow_api/main.py`:
1. Imported `asynccontextmanager` from Python's standard `contextlib`.
2. Created an asynchronous generator function `lifespan(app: FastAPI)` with startup code before `yield` and shutdown code after `yield`.
3. Registered it in the `FastAPI(lifespan=lifespan)` constructor.

---

## 2. Why Did We Do It?
- **Deprecation of Legacy Event Handlers**: Older FastAPI versions used `@app.on_event("startup")` and `@app.on_event("shutdown")`. These are now deprecated in favor of the unified ASGI Lifespan protocol.
- **Unified Lifecycle Management**: Pre-request startup and post-request cleanup logic are collocated in one clean function.
- **Graceful Shutdown**: Guarantees that when your container or server receives a termination signal (`SIGTERM` / `SIGINT`), cleanup code executes before the process exits.

---

## 3. How Does It Work?

```
Server starts (uvicorn taskflow_api.main:app)
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  LIFESPAN: Code BEFORE yield executes        │
│  • Initialize connection pools               │
│  • Load configuration / warm up cache        │
└──────────────────────────────────────────────┘
                  │
                  ▼
                yield  <── Application is LIVE and serving HTTP requests
                  │
                  ▼
Server receives stop signal (Ctrl+C / Docker stop)
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  LIFESPAN: Code AFTER yield executes         │
│  • Close database connection pools           │
│  • Flush logs / metrics                      │
│  • Release file locks / network sockets      │
└──────────────────────────────────────────────┘
                  │
                  ▼
Server process terminates cleanly
```

### Code Implementation:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Startup phase
    print("🚀 [STARTUP]: Initializing services...")
    
    yield  # Application serves traffic
    
    # 2. Shutdown phase
    print("🛑 [SHUTDOWN]: Releasing resources gracefully...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)
```

---

## 4. Real-World Use Cases for Lifespan

| Use Case | Before `yield` (Startup) | After `yield` (Shutdown) |
| :--- | :--- | :--- |
| **Relational Database** | Verify database connectivity | Dispose of database engine connection pool |
| **Redis / Cache** | Open Redis async connection client | Close Redis connection pool |
| **Machine Learning / AI** | Load weights into GPU/RAM once | Unload model weights from memory |
| **Background Schedulers** | Start APScheduler / cron loop | Shut down scheduler threads |
