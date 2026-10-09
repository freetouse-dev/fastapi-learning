import time
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from taskflow_api.routers import health, tasks, auth
from taskflow_api.exceptions import TaskNotFoundError
# from taskflow_api.database import Base, engine
# from taskflow_api.models import task as task_model, user as user_model
from taskflow_api.config import settings

# Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": "TASK_NOT_FOUND",
            "detail": f"Task id {exc.task_id} was not found",
        },
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    print(f"⚡ [PERF]: {request.method} {request.url.path} completed in {process_time * 1000:.2f}ms")

    return response

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(tasks.router)