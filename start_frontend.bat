@echo off
REM Genesis Tauri Frontend Startup Script for Windows

echo.
echo ========================================
echo    Genesis Tauri Frontend Startup
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo Error: Please run this script from the genesis-frontend directory
    echo.
    echo Usage: cd genesis-frontend && start_frontend.bat
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo Error: npm is not installed
    echo Please install npm from https://nodejs.org/
    pause
    exit /b 1
)

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if backend services are running
echo Checking backend services...

REM Check AI Core
curl -s http://127.0.0.1:8000/health >nul 2>&1
if errorlevel 1 (
    echo Warning: AI Core is not running
    echo Please start AI Core first: cd ai_core && start_ai_core.bat
)

REM Check Rust Backend
curl -s http://127.0.0.1:8080/health >nul 2>&1
if errorlevel 1 (
    echo Warning: Rust Backend is not running
    echo Please start Rust Backend: cd backend && start_backend.bat
)

echo.
echo Starting Genesis Tauri Frontend...
echo Frontend will be available at: http://localhost:1420
echo Press Ctrl+C to stop the development server
echo.

npm run tauri dev

pause 