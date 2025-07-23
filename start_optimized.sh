#!/bin/bash
# Optimized Genesis Startup Script (Linux/Mac)

echo "🚀 Starting Genesis (Optimized Mode)..."
echo "======================================"

# Set optimized environment variables
export NODE_ENV=production
export PYTHONOPTIMIZE=1
export RUST_LOG=info
export RUSTFLAGS="-C target-cpu=native"

# Function to check if a service is running
check_service() {
    local url=$1
    local name=$2
    if curl -s "$url" > /dev/null 2>&1; then
        echo "✅ $name is already running"
        return 0
    else
        echo "❌ $name is not running"
        return 1
    fi
}

# Check and start Ollama
echo "🤖 Checking Ollama status..."
if ! check_service "http://localhost:11434/api/tags" "Ollama"; then
    echo "Starting Ollama..."
    ollama serve &
    OLLAMA_PID=$!
    sleep 5
fi

# Start AI Core with optimizations
echo "🧠 Starting AI Core (Optimized)..."
cd ai_core
python -O main.py &
AI_CORE_PID=$!
cd ..

# Wait for AI Core to start
sleep 3

# Start Backend with optimizations
echo "⚙️ Starting Backend (Optimized)..."
cd backend
cargo run --release &
BACKEND_PID=$!
cd ..

# Wait for Backend to start
sleep 3

# Start Frontend with optimizations
echo "🖥️ Starting Frontend (Optimized)..."
cd genesis-frontend
npm run dev:optimized &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Genesis started in optimized mode!"
echo ""
echo "📊 Services:"
echo "  - Ollama: http://localhost:11434"
echo "  - AI Core: http://localhost:8000"
echo "  - Backend: http://localhost:8080"
echo "  - Frontend: http://localhost:5173"
echo ""
echo "🔍 Monitor performance: python scripts/performance_monitor.py"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for all processes
wait 