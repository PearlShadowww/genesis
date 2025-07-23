#!/bin/bash

# Genesis AI Core Startup Script for Linux/macOS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================"
echo "    Genesis AI Core Startup"
echo "========================================"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo -e "${RED}Error: Please run this script from the ai_core directory${NC}"
    echo ""
    echo "Usage: cd ai_core && ./start_ai_core.sh"
    exit 1
fi

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Warning: Some dependencies may not have installed correctly${NC}"
    fi
fi

# Check if Ollama is running
echo -e "${BLUE}Checking Ollama status...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}Ollama is running${NC}"
else
    echo -e "${YELLOW}Warning: Ollama is not running${NC}"
    echo "Please start Ollama with: ollama serve"
    echo ""
    read -p "Continue anyway? (y/N): " continue
    if [[ ! $continue =~ ^[Yy]$ ]]; then
        echo "Startup cancelled"
        exit 1
    fi
fi

# Start the FastAPI server
echo ""
echo -e "${BLUE}Starting Genesis AI Core server...${NC}"
echo -e "${GREEN}Server will be available at: http://127.0.0.1:8000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

uvicorn main:app --host 127.0.0.1 --port 8000 --reload 