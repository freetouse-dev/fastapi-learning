from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from taskflow_api.routers import health, tasks, auth
from taskflow_api.exceptions import TaskNotFoundError
from taskflow_api.database import Base, engine
from taskflow_api.models import task as task_model, user as user_model
from taskflow_api.config import settings

# Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": "TASK_NOT_FOUND",
            "detail": f"Task id {exc.task_id} was not found",
        },
    )

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(tasks.router)