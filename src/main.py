from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Tasker Enterprise API", version="2.0.0")
app.include_router(router, prefix="/api/v1")
