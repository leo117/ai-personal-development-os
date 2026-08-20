from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.core.config import settings
from app.api.router import api_router
from app.db.init_db import seed_database

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Personal Development OS - Phase 1 MVP Backend"
)

# 允许跨域，方便前端连接
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # 自动执行数据库初始化与种子填充
    seed_database()

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "HEALTHY", "version": settings.VERSION}

# 若存在 frontend 静态目录，支持直接挂载
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
