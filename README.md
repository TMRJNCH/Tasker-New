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
