@echo off
REM Genesis Complete Startup Script for Windows

echo.
echo ========================================
echo    Genesis Complete Startup
echo ========================================
echo.

REM Check if we're in the root directory
if not exist "README.md" (
    echo Error: Please run this script from the root Genesis directory
    echo.
    echo Usage: start_all.bat
    pause
    exit /b 1
)

echo Starting all Genesis components...
echo.

REM Start AI Core in a new window
echo Starting AI Core...
start "Genesis AI Core" cmd /k "cd ai_core && start_ai_core.bat"

REM Wait a moment for AI Core to start
timeout /t 5 /nobreak >nul

REM Start Rust Backend in a new window
echo Starting Rust Backend...
start "Genesis Rust Backend" cmd /k "cd backend && start_backend.bat"

REM Wait a moment for Backend to start
timeout /t 5 /nobreak >nul

REM Start Tauri Frontend in a new window
echo Starting Tauri Frontend...
start "Genesis Tauri Frontend" cmd /k "cd genesis-frontend && start_frontend.bat"

echo.
echo All components are starting...
echo.
echo Services will be available at:
echo - AI Core: http://127.0.0.1:8000
echo - Rust Backend: http://127.0.0.1:8080
echo - Tauri Frontend: http://localhost:1420
echo.
echo Press any key to open the frontend in your browser...
pause >nul

REM Open the frontend in the default browser
start http://localhost:1420

echo.
echo Genesis is now running!
echo Close the command windows to stop the services.
pause 