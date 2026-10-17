@echo off
title CloudHire - Starting Servers...
echo.
echo  ==========================================
echo   CloudHire - AI Recruitment Portal
echo   Starting backend and frontend servers...
echo  ==========================================
echo.

:: Start Django Backend
echo [1/2] Starting Django backend on port 8000...
start "CloudHire Backend" /min cmd /k "cd /d C:\Users\Admin\.gemini\antigravity\scratch\cloudhire\backend && venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000"

:: Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

:: Start React Frontend
echo [2/2] Starting React frontend on port 5173...
start "CloudHire Frontend" /min cmd /k "cd /d C:\Users\Admin\.gemini\antigravity\scratch\cloudhire\frontend && npx vite --host 0.0.0.0"

:: Wait for frontend to start
timeout /t 5 /nobreak >nul

echo.
echo  ==========================================
echo   CloudHire is RUNNING!
echo.
echo   Local:   http://localhost:5173
echo   Network: http://192.168.29.62:5173
echo  ==========================================
echo.

:: Open browser automatically
start "" "http://localhost:5173"

echo  Servers are running in background windows.
echo  Close those windows to stop the servers.
echo.
pause
