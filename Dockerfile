FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY README.md ./
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

RUN uv sync --frozen --no-dev

EXPOSE 8080

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn taskflow_api.main:app --host 0.0.0.0 --port 8080"]