from fastapi import APIRouter
from app.api.v1 import sessions, competencies, tasks, research

api_router = APIRouter()

api_router.include_router(sessions.router)
api_router.include_router(competencies.router)
api_router.include_router(tasks.router)
api_router.include_router(research.router)
