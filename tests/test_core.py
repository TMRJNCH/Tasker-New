import pytest
from src.services.manager import TaskManager
from src.domain.models import TaskPriority

@pytest.mark.asyncio
async def test_create_task():
    manager = TaskManager()
    task = await manager.create_task("Test Task", TaskPriority.LOW)
    assert task.title == "Test Task"
    assert task.id is not None

@pytest.mark.asyncio
async def test_high_priority_logic():
    manager = TaskManager()
    task = await manager.create_task("Urgent", TaskPriority.CRITICAL)
    assert task.priority == TaskPriority.CRITICAL
