@echo off
chcp 65001 > nul
echo ============================================================
echo 🚀 AI Personal Development OS (Phase 1 MVP) 正在启动...
echo 📍 前端双工作区访问地址: http://localhost:8000/
echo 📖 OpenAPI 接口文档地址: http://localhost:8000/docs
echo ============================================================

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" run_server.py
) else (
    python run_server.py
)
pause
