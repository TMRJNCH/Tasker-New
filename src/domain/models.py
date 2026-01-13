import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(..., min_length=3)
    description: str = ""
    priority: TaskPriority = TaskPriority.LOW
    is_completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
