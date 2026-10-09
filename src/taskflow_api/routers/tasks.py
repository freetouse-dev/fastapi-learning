from fastapi import APIRouter, status, Path, Query, Depends
from sqlalchemy.orm import Session

from taskflow_api.schemas.task import TaskStatus, TaskCreate, TaskResponse
from taskflow_api.exceptions import TaskNotFoundError
from taskflow_api.models.task import Task
from taskflow_api.database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

TASKS = [
    {
        "id": 1,
        "title": "Setup project environment",
        "status": "completed",
    },
    {
        "id": 2,
        "title": "Create first FastAPI endpoint",
        "status": "completed",
    },
    {
        "id": 3,
        "title": "Learn path parameters",
        "status": "in_progress",
    },
    {
        "id": 4,
        "title": "Learn query parameters",
        "status": "in_progress",
    },
    {
        "id": 5,
        "title": "Understand request body",
        "status": "pending",
    },
    {
        "id": 6,
        "title": "Create Pydantic models",
        "status": "completed",
    },
    {
        "id": 7,
        "title": "Implement POST endpoint",
        "status": "completed",
    },
    {
        "id": 8,
        "title": "Implement PUT endpoint",
        "status": "pending",
    },
    {
        "id": 9,
        "title": "Implement DELETE endpoint",
        "status": "pending",
    },
    {
        "id": 10,
        "title": "Learn dependency injection",
        "status": "in_progress",
    },
    {
        "id": 11,
        "title": "Add request validation",
        "status": "pending",
    },
    {
        "id": 12,
        "title": "Handle API errors",
        "status": "pending",
    },
    {
        "id": 13,
        "title": "Create custom exception handling",
        "status": "pending",
    },
    {
        "id": 14,
        "title": "Learn response models",
        "status": "in_progress",
    },
    {
        "id": 15,
        "title": "Write basic API tests",
        "status": "pending",
    },
]

def pagination_params(
    skip: int = Query(default=0, ge=0, description="skip should be greater than 0"),
    limit: int = Query(default=10, ge=1, le=100, description="limit should be 1-100")
):
    return {
        "skip": skip,
        "limit": limit
    }

@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    status: TaskStatus | None = None, 
    pagination: dict = Depends(pagination_params),
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    if status is not None:
        query = query.filter(Task.status == status)
    return query.offset(pagination["skip"]).limit(pagination["limit"]).all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int = Path(..., ge=0, description="task id should be greater than 0"),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise TaskNotFoundError(task_id)
    return task

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(title=task_data.title, status=task_data.status)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_data: TaskCreate, 
    task_id: int = Path(..., ge=0, description="task id should be greater than 0"),
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise TaskNotFoundError(task_id)
    db_task.title = task_data.title
    db_task.status = task_data.status
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int = Path(..., ge=0, description="task id should be greater than 0"),
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise TaskNotFoundError(task_id)
    db.delete(db_task)
    db.commit()
    return