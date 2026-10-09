from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from taskflow_api.routers import health, tasks
from taskflow_api.exceptions import TaskNotFoundError
from taskflow_api.database import Base, engine
from taskflow_api.models import task as task_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API", version="0.1.0")

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
app.include_router(tasks.router)