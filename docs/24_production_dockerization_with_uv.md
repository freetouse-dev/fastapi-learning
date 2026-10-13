# 24. Production Dockerization with `uv`

A quick reference and revision guide for containerizing a FastAPI application using `uv` and multi-layer caching.

---

## 1. What Did We Do?
We created production container configuration files:
1. Created `.dockerignore` to exclude `.venv`, `.git`, `.env`, tests, and caches from the build context.
2. Created a production `Dockerfile` leveraging the official `ghcr.io/astral-sh/uv:python3.13-bookworm-slim` base image.
3. Implemented two-step layer caching to ensure subsequent image rebuilds take under 1 second.

---

## 2. Why Did We Do It?
- **Portability**: The application runs identically on any developer machine, CI/CD pipeline, and cloud provider (AWS, Google Cloud Run, Render, Kubernetes).
- **Extreme Build Speed**: Using `uv` inside Docker cuts dependency installation times from minutes down to seconds.
- **Layer Caching**: Separating dependency installation from code copying ensures that editing Python source files does not trigger a re-download of third-party wheels.

---

## 3. How Does It Work?

```
1. FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
                  │
                  ▼
2. COPY pyproject.toml uv.lock ./
                  │
                  ▼
3. RUN uv sync --frozen --no-install-project --no-dev
   (Installs third-party wheels ONLY ── CACHED by Docker!)
                  │
                  ▼
4. COPY README.md ./, COPY src ./src, COPY alembic ...
                  │
                  ▼
5. RUN uv sync --frozen --no-dev
   (Installs our local taskflow-api package into the venv)
                  │
                  ▼
6. CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn ..."]
   (Automatically applies pending database migrations BEFORE starting the web server)
```

---

## 4. Why Migrations Must Run on Container Startup

### The Problem:
Inside Docker, the container has its own isolated filesystem. 
Because `.dockerignore` excludes `taskflow.db` (so host dev data is not baked into the image), the container starts with a fresh, empty database.
If you only start Uvicorn without running migrations, the tables (`users`, `tasks`) don't exist yet! When an endpoint executes a query, SQLite throws `no such table: users`.

### The Solution:
In production containers, we execute `alembic upgrade head` before launching Uvicorn:
```dockerfile
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn taskflow_api.main:app --host 0.0.0.0 --port 8080"]
```
Now, whenever a container boots up in AWS, GCP, or Docker:
1. Alembic checks and applies any pending migrations.
2. The database schema is guaranteed to match the code.
3. Uvicorn starts serving traffic safely!

---

## 4. Key Troubleshooting Lesson: Why `README.md` is Required

### The Error:
```
Error: failed to open file `/app/README.md`: No such file or directory
Call to `uv_build.build_editable` failed
```

### The Explanation:
In `pyproject.toml`, line 5 declares:
```toml
readme = "README.md"
```
According to Python packaging standards (PEP 621), when `uv` installs your application package (`taskflow-api`), the build backend (`uv_build`) verifies that all metadata files specified in `pyproject.toml` exist.

Because `README.md` was not copied into the Docker container, the build failed.

### The Fix:
Copy `README.md` along with your source code before `uv sync`:
```dockerfile
COPY README.md ./
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

RUN uv sync --frozen --no-dev
```

---

## 5. Docker Cheat Sheet for This Project

| Action | Command |
| :--- | :--- |
| **Build Image** | `docker build -t taskflow-api .` |
| **Run Container** | `docker run -p 8080:8080 taskflow-api` |
| **Run in Background (Detached)** | `docker run -d -p 8080:8080 --name taskflow taskflow-api` |
| **View Logs** | `docker logs -f taskflow` |
| **Stop Container** | `docker stop taskflow` |
