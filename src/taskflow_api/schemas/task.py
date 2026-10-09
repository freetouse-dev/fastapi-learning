from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=4, max_length=100, description="title of the task")
    status: TaskStatus = TaskStatus.PENDING

class TaskResponse(BaseModel):
    id: int
    title: str
    status: TaskStatus
    owner_id: int

    model_config = ConfigDict(from_attributes=True)