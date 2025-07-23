#!/bin/bash

# Genesis Stop All Script for Linux/macOS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================"
echo "    Genesis Stop All Services"
echo "========================================"
echo -e "${NC}"

# Function to stop a component
stop_component() {
    local name=$1
    local pid_file="logs/${name,,}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${BLUE}Stopping $name (PID: $pid)...${NC}"
            kill "$pid"
            rm "$pid_file"
            echo -e "${GREEN}$name stopped${NC}"
        else
            echo -e "${YELLOW}$name is not running${NC}"
            rm "$pid_file"
        fi
    else
        echo -e "${YELLOW}No PID file found for $name${NC}"
    fi
}

# Stop components
stop_component "AI Core"
stop_component "Rust Backend"
stop_component "Tauri Frontend"

# Kill any remaining Genesis processes
echo -e "${BLUE}Cleaning up any remaining Genesis processes...${NC}"
pkill -f "genesis" || true
pkill -f "uvicorn main:app" || true
pkill -f "cargo run" || true
pkill -f "npm run tauri dev" || true

echo ""
echo -e "${GREEN}All Genesis services have been stopped!${NC}" 