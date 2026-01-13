import os
import subprocess
import time
import sys
from pathlib import Path

REPO_URL = "https://github.com/TMRJNCH/Tasker-New.git"
TG_TOKEN = "YOUR_TOKEN"
TG_CHAT_ID = "YOUR_CHAT_ID"

def run_cmd(command, ignore_errors=False):
    print(f"Exec: {command}")
    try:
        subprocess.run(command, shell=True, check=not ignore_errors)
        time.sleep(0.5)
    except subprocess.CalledProcessError:
        if not ignore_errors:
            sys.exit(1)

def create_file(path_str, content):
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

create_file("requirements.txt", """
fastapi>=0.109.0
uvicorn>=0.27.0
pydantic>=2.6.0
pydantic-settings>=2.1.0
requests>=2.31.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.26.0
""")

create_file(".gitignore", """
__pycache__/
*.pyc
.env
venv/
.pytest_cache/
""")

create_file("README.md", """
# Tasker Enterprise System

## Architecture
- **Domain**: Business Entities (Pydantic Models)
- **Infrastructure**: Data Access (Repository Pattern)
- **Services**: Business Logic & Integrations
- **API**: REST Controllers (FastAPI)

## Tech Stack
- Python 3.10+
- FastAPI
- Pydantic V2
- Pytest
- GitHub Actions

## Run
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```
""")

create_file("src/__init__.py", "")
create_file("src/domain/__init__.py", "")
create_file("src/domain/models.py", """
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
""")

create_file("src/infrastructure/__init__.py", "")
create_file("src/infrastructure/repository.py", """
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
""")

create_file("src/services/__init__.py", "")
create_file("src/services/telegram.py", f"""
import requests
import logging

class TelegramService:
    def __init__(self):
        self.token = "{TG_TOKEN}"
        self.chat_id = "{TG_CHAT_ID}"
    
    def send_notification(self, message: str):
        if "YOUR_" in self.token:
            return

        url = f"https://api.telegram.org/bot{{self.token}}/sendMessage"
        try:
            requests.post(url, json={{"chat_id": self.chat_id, "text": message}})
        except Exception:
            pass
""")

create_file("src/services/manager.py", """
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
""")

create_file("src/api/__init__.py", "")
create_file("src/api/routes.py", """
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
""")

create_file("src/main.py", """
from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Tasker Enterprise API", version="2.0.0")
app.include_router(router, prefix="/api/v1")
""")

create_file("tests/__init__.py", "")
create_file("tests/test_core.py", """
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
""")

create_file(".github/workflows/ci.yml", """
name: Enterprise CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    - run: pip install -r requirements.txt
    - run: pytest tests/
""")

run_cmd("git init")
run_cmd("git config user.name 'DevOps'")
run_cmd("git config user.email 'devops@tasker.internal'")

run_cmd("git add .")
run_cmd("git commit -m 'Initial commit: Project scaffold'")

run_cmd("git checkout -b feature/domain")
create_file("domain.txt", "Domain Logic v1")
run_cmd("git add domain.txt")
run_cmd("git commit -m 'Docs: Domain'")
run_cmd("git checkout main")
run_cmd("git merge feature/domain")
run_cmd("git branch -d feature/domain")

create_file("config.txt", "VERSION=1.0")
run_cmd("git add config.txt")
run_cmd("git commit -m 'Add config'")

run_cmd("git checkout -b feature/update")
create_file("config.txt", "VERSION=2.0-BETA")
run_cmd("git add config.txt")
run_cmd("git commit -m 'Bump version beta'")

run_cmd("git checkout main")
create_file("config.txt", "VERSION=1.1-STABLE")
run_cmd("git add config.txt")
run_cmd("git commit -m 'Hotfix stable'")

run_cmd("git merge feature/update", ignore_errors=True) 

create_file("config.txt", "VERSION=2.0-FINAL")
run_cmd("git add config.txt")
run_cmd("git commit -m 'Merge conflict resolved'")

run_cmd("git add .github")
run_cmd("git commit -m 'CI/CD: GitHub Actions'")

run_cmd("git add src tests")
run_cmd("git commit -m 'Feat: Clean Architecture Implementation'")

run_cmd("git remote remove origin", ignore_errors=True)
run_cmd(f"git remote add origin {REPO_URL}")
run_cmd("git branch -M main")
run_cmd("git push -u origin main")
