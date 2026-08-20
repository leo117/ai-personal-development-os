"""
AI Personal Development OS - 启动入口脚本
一键启动 FastAPI 后端服务并挂载 Web 双工作区前端
"""
import sys
import os
import uvicorn

# 将 backend 路径添加到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AI Personal Development OS (Phase 1 MVP) 正在启动...")
    print("📍 前端双工作区访问地址: http://localhost:8000/")
    print("📖 OpenAPI 接口文档地址: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        app_dir="backend"
    )
