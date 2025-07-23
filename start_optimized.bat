@echo off
REM Optimized Genesis Startup Script (Windows)

echo 🚀 Starting Genesis (Optimized Mode)...
echo ======================================

REM Set optimized environment variables
set NODE_ENV=production
set PYTHONOPTIMIZE=1
set RUST_LOG=info
set RUSTFLAGS=-C target-cpu=native

REM Check if Ollama is running
echo 🤖 Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo Starting Ollama...
    start /B ollama serve
    timeout /t 5 /nobreak >nul
) else (
    echo ✅ Ollama is already running
)

REM Start AI Core with optimizations
echo 🧠 Starting AI Core (Optimized)...
cd ai_core
start /B python -O main.py
cd ..

REM Wait for AI Core to start
timeout /t 3 /nobreak >nul

REM Start Backend with optimizations
echo ⚙️ Starting Backend (Optimized)...
cd backend
start /B cargo run --release
cd ..

REM Wait for Backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend with optimizations
echo 🖥️ Starting Frontend (Optimized)...
cd genesis-frontend
start /B npm run dev:optimized
cd ..

echo.
echo ✅ Genesis started in optimized mode!
echo.
echo 📊 Services:
echo   - Ollama: http://localhost:11434
echo   - AI Core: http://localhost:8000
echo   - Backend: http://localhost:8080
echo   - Frontend: http://localhost:5173
echo.
echo 🔍 Monitor performance: python scripts/performance_monitor.py
echo.
pause 