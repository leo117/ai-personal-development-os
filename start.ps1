# AI Personal Development OS - PowerShell 启动脚本
$OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 AI Personal Development OS (Phase 1 MVP) 正在启动..." -ForegroundColor Green
Write-Host "📍 前端双工作区访问地址: http://localhost:8000/" -ForegroundColor Yellow
Write-Host "📖 OpenAPI 接口文档地址: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

if (Test-Path ".\.venv\Scripts\python.exe") {
    & ".\.venv\Scripts\python.exe" run_server.py
} else {
    python run_server.py
}
