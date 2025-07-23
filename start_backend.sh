#!/bin/bash

# Genesis Rust Backend Startup Script for Linux/macOS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================"
echo "    Genesis Rust Backend Startup"
echo "========================================"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo -e "${RED}Error: Please run this script from the backend directory${NC}"
    echo ""
    echo "Usage: cd backend && ./start_backend.sh"
    exit 1
fi

# Check if Rust is installed
if ! command -v rustc &> /dev/null; then
    echo -e "${RED}Error: Rust is not installed${NC}"
    echo "Please install Rust from https://rustup.rs/"
    exit 1
fi

# Build the project
echo -e "${BLUE}Building Rust backend...${NC}"
cargo build --release
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Build failed${NC}"
    exit 1
fi

# Check if AI Core is running
echo -e "${BLUE}Checking AI Core status...${NC}"
if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}AI Core is running${NC}"
else
    echo -e "${YELLOW}Warning: AI Core is not running${NC}"
    echo "Please start AI Core first: cd ai_core && ./start_ai_core.sh"
    echo ""
    read -p "Continue anyway? (y/N): " continue
    if [[ ! $continue =~ ^[Yy]$ ]]; then
        echo "Startup cancelled"
        exit 1
    fi
fi

# Start the Rust server
echo ""
echo -e "${BLUE}Starting Genesis Rust Backend server...${NC}"
echo -e "${GREEN}Server will be available at: http://127.0.0.1:8080${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

cargo run --release
```

```batch:start_frontend.bat
@echo off
REM Genesis Tauri Frontend Startup Script for Windows

echo.
echo ====================================== 