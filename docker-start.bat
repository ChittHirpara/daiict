@echo off
REM Docker startup script for Windows
title VERITAS Command Center - Docker

echo =========================================
echo   VERITAS Command Center - Docker Setup
echo =========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed!
    echo Please install Docker Desktop: https://docs.docker.com/desktop/windows/install/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed!
    echo Please install Docker Desktop which includes Docker Compose
    pause
    exit /b 1
)

echo Docker and Docker Compose found
echo.

echo Building Docker images...
docker-compose build

echo.
echo Starting containers...
docker-compose up -d

echo.
echo =========================================
echo   Services Starting...
echo =========================================
echo.
echo Waiting for services to be ready...
timeout /t 5 /nobreak >nul

echo.
echo Checking service status...
docker-compose ps

echo.
echo =========================================
echo   VERITAS Command Center is running!
echo =========================================
echo.
echo Access points:
echo    API:        http://localhost:8000/docs
echo    Dashboard:  http://localhost:8501
echo.
echo Useful commands:
echo    View logs:    docker-compose logs -f
echo    Stop:         docker-compose down
echo    Restart:      docker-compose restart
echo    Status:       docker-compose ps
echo.
pause
