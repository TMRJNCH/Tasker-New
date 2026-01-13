from typing import List, Optional
import uuid
from src.domain.models import Task

class InMemoryTaskRepository:
    def __init__(self):
        self._db: List[Task] = []

    async def save(self, task: Task) -> Task:
        self._db.append(task)
        return task

    async def get_all(self) -> List[Task]:
        return self._db

    async def get_by_id(self, task_id: uuid.UUID) -> Optional[Task]:
        return next((t for t in self._db if t.id == task_id), None)

    async def delete(self, task_id: uuid.UUID) -> bool:
        initial_count = len(self._db)
        self._db = [t for t in self._db if t.id != task_id]
        return len(self._db) < initial_count
