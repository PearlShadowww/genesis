#!/bin/bash

# Genesis Tauri Frontend Startup Script for Linux/macOS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================"
echo "    Genesis Tauri Frontend Startup"
echo "========================================"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo -e "${RED}Error: Please run this script from the genesis-frontend directory${NC}"
    echo ""
    echo "Usage: cd genesis-frontend && ./start_frontend.sh"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed${NC}"
    echo "Please install npm from https://nodejs.org/"
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Installing Node.js dependencies...${NC}"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install dependencies${NC}"
        exit 1
    fi
fi

# Check if backend services are running
echo -e "${BLUE}Checking backend services...${NC}"

# Check AI Core
if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}AI Core is running${NC}"
else
    echo -e "${YELLOW}Warning: AI Core is not running${NC}"
    echo "Please start AI Core first: cd ai_core && ./start_ai_core.sh"
fi

# Check Rust Backend
if curl -s http://127.0.0.1:8080/health > /dev/null 2>&1; then
    echo -e "${GREEN}Rust Backend is running${NC}"
else
    echo -e "${YELLOW}Warning: Rust Backend is not running${NC}"
    echo "Please start Rust Backend: cd backend && ./start_backend.sh"
fi

echo ""
echo -e "${BLUE}Starting Genesis Tauri Frontend...${NC}"
echo -e "${GREEN}Frontend will be available at: http://localhost:1420${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the development server${NC}"
echo ""

npm run tauri dev 