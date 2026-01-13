from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from src.domain.models import Task, TaskPriority
from src.services.manager import TaskManager

router = APIRouter()
manager = TaskManager()

class TaskCreateRequest(BaseModel):
    title: str
    priority: TaskPriority = TaskPriority.LOW

@router.post("/tasks", response_model=Task)
async def create_task(dto: TaskCreateRequest):
    return await manager.create_task(dto.title, dto.priority)

@router.get("/tasks", response_model=List[Task])
async def get_tasks():
    return await manager.get_tasks()
