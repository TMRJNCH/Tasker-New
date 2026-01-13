from src.domain.models import Task, TaskPriority
from src.infrastructure.repository import InMemoryTaskRepository
from src.services.telegram import TelegramService

class TaskManager:
    def __init__(self):
        self.repo = InMemoryTaskRepository()
        self.notifier = TelegramService()

    async def create_task(self, title: str, priority: TaskPriority) -> Task:
        new_task = Task(title=title, priority=priority)
        saved = await self.repo.save(new_task)
        
        if priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]:
            self.notifier.send_notification(f"Important Task: {title}")
        
        return saved

    async def get_tasks(self):
        return await self.repo.get_all()
