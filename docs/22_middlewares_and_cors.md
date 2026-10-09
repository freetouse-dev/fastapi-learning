# 22. Middlewares & CORS (Cross-Origin Resource Sharing)

A quick reference and revision guide for understanding HTTP middleware pipelines and configuring CORS in FastAPI.

---

## 1. What Did We Do?
We implemented global request interceptors in `src/taskflow_api/main.py`:
1. Configured **`CORSMiddleware`** to allow frontend clients (React on port 3000, Vite on port 5173, Angular on port 4200) to communicate with our API without browser security blocks.
2. Created a custom **HTTP Timing Middleware** using `@app.middleware("http")` that measures execution time in milliseconds, logs performance, and injects a custom response header `X-Process-Time`.

---

## 2. Why Did We Do It?

### A. CORS (Browser Security)
Web browsers enforce the **Same-Origin Policy**. If a frontend on `http://localhost:3000` attempts to call an API on `http://127.0.0.1:8000`, the browser rejects the response unless the server explicitly returns `Access-Control-Allow-Origin` headers. `CORSMiddleware` automates this negotiation.

### B. Custom Middleware (Global Observability)
Middleware runs around the entire HTTP lifecycle:
- Intercepts requests **before** any router or dependency executes.
- Intercepts responses **after** route logic finishes.
- Enables timing, request logging, request ID tracking, and security header injection across all endpoints from a single place.

---

## 3. How Does It Work?

```
Client sends Request
         │
         ▼
[Custom Timing Middleware] ──> Starts high-resolution timer (time.perf_counter())
         │
         ▼
[CORSMiddleware] ────────────> Checks Origin header against allowed whitelist
         │
         ▼
[FastAPI Router & DB] ───────> Executes route handler & returns Response
         │
         ▼
[CORSMiddleware] ────────────> Injects Access-Control-* headers into Response
         │
         ▼
[Custom Timing Middleware] ──> Computes duration, attaches X-Process-Time header, logs duration
         │
         ▼
Client receives Response with X-Process-Time: 0.0014s
```

### Code Implementation:

```python
from fastapi.middleware.cors import CORSMiddleware

# 1. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Custom Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)  # Passes request to route handler
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    print(f"⚡ [PERF]: {request.method} {request.url.path} in {process_time * 1000:.2f}ms")
    return response
```

---

## 4. Production Best Practices for CORS
- **Never use `allow_origins=["*"]` with `allow_credentials=True`**: Modern browsers reject wildcards when cookies or Authorization headers are sent.
- **Store Allowed Origins in Configuration**: In production, read origins from `settings.ALLOWED_ORIGINS` in `.env` so you can configure different domains for staging and production.
