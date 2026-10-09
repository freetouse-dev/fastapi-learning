# 16. Configuration & Environment Management (`pydantic-settings`)

A quick reference and revision guide for managing environment variables and application configurations cleanly in FastAPI.

---

## 1. What Did We Do?
We introduced centralized, type-safe configuration management:
1. Installed `pydantic-settings` with `uv add pydantic-settings`.
2. Created `config.py` with a `Settings` class inheriting from `BaseSettings`.
3. Created a `.env` file for local development settings.
4. Updated `main.py` and `database.py` to consume dynamic values from `settings`.

---

## 2. Why Did We Do It?
- **12-Factor App Compliance**: Strictly separates code from environment configuration.
- **Security**: Database passwords, JWT secret keys, and cloud credentials should never be committed to Git. They stay in `.env`.
- **Environment Flexibility**: Easily switch between environments (e.g. SQLite for local dev, PostgreSQL for staging/production) without modifying application code.
- **Fail-Fast Type Safety**: If an environment variable is invalid or missing, Pydantic fails immediately on startup with a descriptive error.

---

## 3. How Does It Work?

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskFlow API"
    VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///./taskflow.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
```

### Configuration Priority (Highest to Lowest):
1. **OS Environment Variables** (e.g., set via Docker, Kubernetes, or terminal `export DATABASE_URL=...`)
2. **Variables defined in `.env`**
3. **Default values declared in Python** (e.g. `VERSION: str = "0.1.0"`)

---

## 4. Best Practices
1. **Always ignore `.env` in Git**: Ensure `.env` is listed in `.gitignore`.
2. **Commit `.env.example`**: Maintain `.env.example` with dummy values so teammates know what environment variables are required.
3. **Use `extra="ignore"`**: Prevents unexpected system variables from crashing Pydantic's validator.
