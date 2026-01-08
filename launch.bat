@echo off
title VERITAS Command Center Launcher
color 0A

echo ========================================
echo   VERITAS AI Regulatory Command Center
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo       Python OK
echo.

echo [2/5] Checking dependencies...
python -c "import streamlit, fastapi" >nul 2>&1
if errorlevel 1 (
    echo       Installing dependencies...
    pip install -r requirements_upgraded.txt
)
echo       Dependencies OK
echo.

echo [3/5] Setting up database...
python setup_database.py
echo       Database OK
echo.

echo [4/5] Starting API server...
start "VERITAS API Server" cmd /k "cd /d %~dp0 && python api/main.py"
timeout /t 3 >nul
echo       API Server started at http://localhost:8000
echo.

echo [5/5] Starting Command Center Dashboard...
start "VERITAS Dashboard" cmd /k "cd /d %~dp0 && streamlit run dashboard.py"
timeout /t 2 >nul
echo       Dashboard starting at http://localhost:8501
echo.

echo ========================================
echo   LAUNCH COMPLETE!
echo ========================================
echo.
echo   API:        http://localhost:8000/docs
echo   Dashboard:  http://localhost:8501
echo.
echo   Press any key to exit...
pause >nul
