#!/bin/bash

# Genesis Complete Startup Script for Linux/macOS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================"
echo "    Genesis Complete Startup"
echo "========================================"
echo -e "${NC}"

# Check if we're in the root directory
if [ ! -f "README.md" ]; then
    echo -e "${RED}Error: Please run this script from the root Genesis directory${NC}"
    echo ""
    echo "Usage: ./start_all.sh"
    exit 1
fi

echo -e "${BLUE}Starting all Genesis components...${NC}"
echo ""

# Function to start a component in background
start_component() {
    local name=$1
    local script=$2
    local dir=$3
    
    echo -e "${BLUE}Starting $name...${NC}"
    
    # Create log directory if it doesn't exist
    mkdir -p logs
    
    # Start component in background and save PID
    cd "$dir" && nohup ./"$script" > "../logs/${name,,}.log" 2>&1 &
    local pid=$!
    echo $pid > "../logs/${name,,}.pid"
    cd ..
    
    echo -e "${GREEN}$name started (PID: $pid)${NC}"
    sleep 3
}

# Make scripts executable
chmod +x ai_core/start_ai_core.sh
chmod +x backend/start_backend.sh
chmod +x genesis-frontend/start_frontend.sh

# Start components
start_component "AI Core" "start_ai_core.sh" "ai_core"
start_component "Rust Backend" "start_backend.sh" "backend"
start_component "Tauri Frontend" "start_frontend.sh" "genesis-frontend"

echo ""
echo -e "${GREEN}All components are starting...${NC}"
echo ""
echo -e "${BLUE}Services will be available at:${NC}"
echo -e "  - AI Core: ${GREEN}http://127.0.0.1:8000${NC}"
echo -e "  - Rust Backend: ${GREEN}http://127.0.0.1:8080${NC}"
echo -e "  - Tauri Frontend: ${GREEN}http://localhost:1420${NC}"
echo ""

# Wait for services to be ready
echo -e "${BLUE}Waiting for services to be ready...${NC}"
for i in {1..30}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1 && \
       curl -s http://127.0.0.1:8080/health > /dev/null 2>&1; then
        echo -e "${GREEN}All services are ready!${NC}"
        break
    fi
    echo -n "."
    sleep 2
done

echo ""
echo -e "${GREEN}Genesis is now running!${NC}"
echo ""
echo -e "${YELLOW}To stop all services, run: ./stop_all.sh${NC}"
echo -e "${YELLOW}To view logs, check the logs/ directory${NC}"
echo ""

# Try to open the frontend in the default browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:1420
elif command -v open &> /dev/null; then
    open http://localhost:1420
fi 