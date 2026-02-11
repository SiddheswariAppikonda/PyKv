@echo off
title Start All PyKV Servers
echo 🚀 Starting all PyKV servers...

:: --- Set PYTHONPATH to project root ---
set PYTHONPATH=%CD%

:: --- Start Primary KV Server ---
start "KV Primary Server" cmd /k python -m uvicorn kv_primary:app --reload --port 8000 --app-dir .

timeout /t 2 > nul

:: --- Start Replica KV Server ---
start "KV Replica Server" cmd /k python -m uvicorn kv_replica:app --reload --port 8001 --app-dir .

timeout /t 2 > nul

:: --- Start Auth Service ---
start "Auth Service" cmd /k python -m uvicorn auth_service.main:app --reload --port 8002 --app-dir .

echo ✅ All servers started successfully!
pause

