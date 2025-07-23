@echo off
echo.
echo ========================================
echo    Genesis Development Startup
echo ========================================
echo.

echo Starting Genesis development environment...
echo This will start the AI Core backend and Frontend development server.
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Python and Node.js are available
echo.

REM Start AI Core in background
echo 🤖 Starting AI Core backend...
cd ai_core
start "Genesis AI Core" cmd /c "python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"
cd ..

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend
echo 🌐 Starting Frontend development server...
cd genesis-frontend
start "Genesis Frontend" cmd /c "npm run dev"
cd ..

echo.
echo 🎉 Genesis development environment is starting!
echo.
echo 📊 Services:
echo - AI Core Backend: http://127.0.0.1:8000
echo - Frontend Dev Server: http://localhost:5173
echo.
echo 🔗 Testing connection in 5 seconds...
timeout /t 5 /nobreak >nul

REM Test connection
node test_frontend_backend.js

echo.
echo 💡 Instructions:
echo 1. Open your browser to http://localhost:5173
echo 2. Check that the status shows "Connected" in the top right
echo 3. Enter a project description and click "Generate Project"
echo.
echo Press any key to exit...
pause >nul 