# 01. Project Setup with `uv`

A quick reference and revision guide for setting up and managing a FastAPI project using `uv`.

---

## 1. What Did We Do?
We initialized a new Python project named `taskflow-api` using `uv` as the package and project manager, and installed `fastapi` and `uvicorn`.

---

## 2. Why Did We Use `uv`?

| Traditional `pip + venv` | Modern `uv` |
| :--- | :--- |
| Manual environment creation (`python -m venv .venv`). | Automatic environment creation on demand. |
| Slow installation speeds (sequential pip wheel downloads). | Extremely fast (10x–100x faster, written in Rust). |
| No native lockfile (`pip freeze` mixes direct and indirect dependencies). | Deterministic lockfile (`uv.lock`) guarantees the same build across all machines. |
| Scattered config files (`requirements.txt`, `runtime.txt`, etc.). | Single standardized `pyproject.toml` file (PEP 517/621). |

---

## 3. Step-by-Step Setup Commands

### Step 1: Initialize the Application
```bash
uv init taskflow-api --app
```
- **What it does**: Creates a new project directory with standard project layout (`src/` layout) and creates `pyproject.toml`.
- **The `--app` flag**: Configures the project as an deployable application rather than a reusable library package.

### Step 2: Navigate into the Project
```bash
cd taskflow-api
```

### Step 3: Add Dependencies
```bash
uv add fastapi "uvicorn[standard]"
```
- **What it does**:
  1. Creates `.venv` automatically if it doesn't already exist.
  2. Resolves compatible package versions.
  3. Downloads and installs `fastapi` and `uvicorn`.
  4. Records direct dependencies in `pyproject.toml`.
  5. Pins exact versions and checksums in `uv.lock`.

---

## 4. Understanding the Generated Files

| File / Folder | Purpose |
| :--- | :--- |
| **`pyproject.toml`** | The central project manifest. Defines project name, Python version requirements, and direct dependencies. |
| **`uv.lock`** | The deterministic lockfile. Contains exact versions and integrity hashes of all packages (both direct and transitive). Never edit this manually. |
| **`.python-version`** | Specifies the exact Python version pinned for this project. |
| **`.venv/`** | The isolated virtual environment containing installed Python packages. |
| **`src/taskflow_api/`** | The source code root for our application. Using a `src/` layout prevents accidental imports of uninstalled code. |

---

## 5. Daily `uv` Cheat Sheet

| Task | Command |
| :--- | :--- |
| Run any command inside the environment | `uv run <command>` (e.g. `uv run uvicorn ...`) |
| Add a production dependency | `uv add <package>` |
| Add a development/testing dependency | `uv add --dev pytest httpx` |
| Remove a dependency | `uv remove <package>` |
| Sync environment to match `uv.lock` | `uv sync` |
