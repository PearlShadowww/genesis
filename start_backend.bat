@echo off
REM Genesis Rust Backend Startup Script for Windows

echo.
echo ========================================
echo    Genesis Rust Backend Startup
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "Cargo.toml" (
    echo Error: Please run this script from the backend directory
    echo.
    echo Usage: cd backend && start_backend.bat
    pause
    exit /b 1
)

REM Check if Rust is installed
rustc --version >nul 2>&1
if errorlevel 1 (
    echo Error: Rust is not installed
    echo Please install Rust from https://rustup.rs/
    pause
    exit /b 1
)

REM Build the project
echo Building Rust backend...
cargo build --release
if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

REM Check if AI Core is running
echo Checking AI Core status...
curl -s http://127.0.0.1:8000/health >nul 2>&1
if errorlevel 1 (
    echo Warning: AI Core is not running
    echo Please start AI Core first: cd ai_core && start_ai_core.bat
    echo.
    set /p continue="Continue anyway? (y/N): "
    if /i not "%continue%"=="y" (
        echo Startup cancelled
        pause
        exit /b 1
    )
) else (
    echo AI Core is running
)

REM Start the Rust server
echo.
echo Starting Genesis Rust Backend server...
echo Server will be available at: http://127.0.0.1:8080
echo Press Ctrl+C to stop the server
echo.

cargo run --release

pause 