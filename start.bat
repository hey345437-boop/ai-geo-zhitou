@echo off
REM 智投 - Windows一键启动脚本
REM 此脚本用于设置和启动整个应用程序

echo ==========================================
echo   智投 - 一键启动
echo ==========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed
    echo Please install Docker Desktop from https://www.docker.com/get-started
    pause
    exit /b 1
)

REM Check if Docker Desktop is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is not running
    echo.
    echo Please start Docker Desktop and wait for it to be ready, then run this script again.
    echo.
    echo Steps:
    echo 1. Open Docker Desktop
    echo 2. Wait for the whale icon to stop animating
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed
    echo Please install Docker Compose
    pause
    exit /b 1
)

REM Check if .env exists, if not copy from example
if not exist .env (
    echo [INFO] Creating .env file from .env.example...
    copy .env.example .env
    echo [SUCCESS] .env file created
    echo.
    echo [INFO] You can edit .env file with your API keys if needed
    echo       The application will work with mock data without API keys
    echo.
)

echo.
echo Step 1: Stopping any existing containers...
docker-compose down 2>nul
echo [SUCCESS] Cleaned up existing containers

echo.
echo Step 2: Building Docker images (this may take a few minutes)...
docker-compose build
if errorlevel 1 (
    echo [ERROR] Failed to build Docker images
    pause
    exit /b 1
)
echo [SUCCESS] Docker images built

echo.
echo Step 3: Starting services...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)
echo [SUCCESS] Services started

echo.
echo Step 4: Waiting for services to be ready...
echo This may take 30-60 seconds...
timeout /t 30 /nobreak >nul

echo.
echo ==========================================
echo   智投现在正在运行！
echo ==========================================
echo.
echo 访问应用程序:
echo   前端界面:        http://localhost:5173
echo   后端API:         http://localhost:8000
echo   API文档:         http://localhost:8000/docs
echo   RabbitMQ:        http://localhost:15672 (guest/guest)
echo   Neo4j浏览器:     http://localhost:7474 (neo4j/your_secure_password)
echo.
echo 常用命令:
echo   查看日志:        docker-compose logs -f
echo   停止服务:        docker-compose down
echo   重启服务:        docker-compose restart
echo.
echo 正在浏览器中打开前端界面...
timeout /t 3 /nobreak >nul
start http://localhost:5173
echo.
echo Press any key to view logs (Ctrl+C to exit logs)...
pause >nul
docker-compose logs -f
