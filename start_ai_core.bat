@echo off
REM Genesis AI Core Startup Script for Windows

echo.
echo ========================================
echo    Genesis AI Core Startup
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo Error: Please run this script from the ai_core directory
    echo.
    echo Usage: cd ai_core && start_ai_core.bat
    pause
    exit /b 1
)

REM Check if Python virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing Python dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Warning: Some dependencies may not have installed correctly
    )
)

REM Check if Ollama is running
echo Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo Warning: Ollama is not running
    echo Please start Ollama with: ollama serve
    echo.
    set /p continue="Continue anyway? (y/N): "
    if /i not "%continue%"=="y" (
        echo Startup cancelled
        pause
        exit /b 1
    )
) else (
    echo Ollama is running
)

REM Start the FastAPI server
echo.
echo Starting Genesis AI Core server...
echo Server will be available at: http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --host 127.0.0.1 --port 8000 --reload

pause 