from fastapi import APIRouter, status, Path, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from taskflow_api.schemas.task import TaskStatus, TaskCreate, TaskResponse
from taskflow_api.exceptions import TaskNotFoundError
from taskflow_api.models.task import Task
from taskflow_api.database import get_db
from taskflow_api.models.user import User
from taskflow_api.security import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

def pagination_params(
    skip: int = Query(default=0, ge=0, description="skip should be greater than 0"),
    limit: int = Query(default=10, ge=1, le=100, description="limit should be 1-100")
):
    return {"skip": skip, "limit": limit}

@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    status: TaskStatus | None = None, 
    pagination: dict = Depends(pagination_params),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Task).filter(Task.owner_id == current_user.id)
    if status is not None:
        query = query.filter(Task.status == status)
    return query.offset(pagination["skip"]).limit(pagination["limit"]).all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int = Path(..., ge=0, description="task id should be greater than 0"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise TaskNotFoundError(task_id)
    
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have a permission to access this task"
        )
    return task

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(
    task_data: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = Task(
        title=task_data.title, 
        status=task_data.status,
        owner_id=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_data: TaskCreate, 
    task_id: int = Path(..., ge=0, description="task id should be greater than 0"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise TaskNotFoundError(task_id)
    if db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have a permission to modify this task"
        )
    db_task.title = task_data.title
    db_task.status = task_data.status
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int = Path(..., ge=0, description="task id should be greater than 0"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise TaskNotFoundError(task_id)
    if db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have a permission to delete this task"
        )

    db.delete(db_task)
    db.commit()
    return