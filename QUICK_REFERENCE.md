# Genesis Quick Reference Card

## 🚀 Quick Start Commands

### **Start All Services**
```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: AI Core
cd ai_core && python main.py

# Terminal 3: Backend
cd backend && cargo run

# Terminal 4: Frontend
cd genesis-frontend && npm run tauri dev
```

### **Stop All Services**
```bash
# Windows
taskkill /F /IM python.exe
taskkill /F /IM node.exe
taskkill /F /IM ollama.exe

# Linux/Mac
pkill -f python
pkill -f node
pkill -f ollama
```

---

## 🔍 Health Check Commands

### **Quick Status Check**
```bash
# All services in one command
curl -s http://localhost:5173 > /dev/null && echo "✅ Frontend" || echo "❌ Frontend"
curl -s http://localhost:8080/health > /dev/null && echo "✅ Backend" || echo "❌ Backend"
curl -s http://localhost:8000/health > /dev/null && echo "✅ AI Core" || echo "❌ AI Core"
curl -s http://localhost:11434/api/tags > /dev/null && echo "✅ Ollama" || echo "❌ Ollama"
```

### **Detailed Health Check**
```bash
# Frontend
curl http://localhost:5173

# Backend
curl http://localhost:8080/health

# AI Core
curl http://localhost:8000/health

# Ollama
curl http://localhost:11434/api/tags
```

---

## 🧪 Testing Commands

### **Test Generation**
```bash
# Test backend generation
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Create a simple React counter","backend":"ollama"}'

# Test AI core directly
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Create a simple React counter","backend":"ollama"}'
```

### **Test LLM**
```bash
# Test Ollama models
cd ai_core
python test_ollama.py

# Test CrewAI integration
python test_llm_crewai.py

# Debug components
python debug_test.py
```

---

## 🔧 Troubleshooting Commands

### **Port Issues**
```bash
# Check what's using ports
netstat -ano | findstr :8000
netstat -ano | findstr :8080
netstat -ano | findstr :5173

# Kill process by PID
taskkill /F /PID <PID>
```

### **Dependency Issues**
```bash
# Python dependencies
cd ai_core
pip install -r requirements.txt

# Rust dependencies
cd backend
cargo build

# Node dependencies
cd genesis-frontend
npm install
```

### **Ollama Issues**
```bash
# Check models
ollama list

# Pull models
ollama pull qwen2.5-coder:1.5b-base
ollama pull llama3.1:8b

# Test model
ollama run qwen2.5-coder:1.5b-base "Hello"
```

---

## 📊 Service Information

### **Service Ports**
| Service | Port | URL |
|---------|------|-----|
| Frontend | 5173 | http://localhost:5173 |
| Backend | 8080 | http://localhost:8080 |
| AI Core | 8000 | http://localhost:8000 |
| Ollama | 11434 | http://localhost:11434 |

### **API Endpoints**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service health check |
| `/generate` | POST | Start project generation |
| `/projects/{id}` | GET | Get project status |
| `/run` | POST | AI Core generation |

### **Environment Variables**
```bash
# Required
AI_CORE_URL=http://127.0.0.1:8000
BACKEND_URL=http://127.0.0.1:8080
OLLAMA_URL=http://localhost:11434

# Optional
AI_CORE_PORT=8000
BACKEND_PORT=8080
FRONTEND_PORT=5173
OLLAMA_MODEL=qwen2.5-coder:1.5b-base
```

---

## 🚨 Common Issues & Quick Fixes

### **"LLM Failed" Error**
```python
# In ai_core/main.py, disable memory
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,
    memory=False  # Add this line
)
```

### **"Connection refused" Error**
```bash
# Start Ollama
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### **"Port already in use" Error**
```bash
# Find and kill process
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

### **"Validation error" Error**
```bash
# Check request format
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test","backend":"ollama"}'
```

---

## 📁 Key Files

### **Configuration Files**
- `ai_core/requirements.txt` - Python dependencies
- `backend/Cargo.toml` - Rust dependencies
- `genesis-frontend/package.json` - Node dependencies
- `env.example` - Environment template

### **Core Files**
- `ai_core/main.py` - AI Core server
- `ai_core/llm.py` - LLM configuration
- `backend/src/main.rs` - Backend server
- `genesis-frontend/src/App.tsx` - Frontend app

### **Testing Files**
- `ai_core/test_ollama.py` - Ollama tests
- `ai_core/debug_test.py` - Debug tests
- `tests/test_integration.py` - Integration tests

---

## 🔄 Recovery Procedures

### **Complete Reset**
```bash
# 1. Stop all services
taskkill /F /IM python.exe
taskkill /F /IM node.exe
taskkill /F /IM ollama.exe

# 2. Start in order
ollama serve
cd ai_core && python main.py &
cd backend && cargo run &
cd genesis-frontend && npm run tauri dev &
```

### **Service-Specific Reset**
```bash
# AI Core
cd ai_core
pip install -r requirements.txt --force-reinstall
python main.py

# Backend
cd backend
cargo clean && cargo build
cargo run

# Frontend
cd genesis-frontend
rm -rf node_modules && npm install
npm run tauri dev
```

---

## 📞 Emergency Commands

### **System Information**
```bash
# Check system resources
top
htop
tasklist

# Check network
netstat -an
netstat -ano | findstr :8000

# Check disk space
df -h
dir
```

### **Log Access**
```bash
# AI Core logs
# Check console output

# Backend logs
# Check console output

# Frontend logs
# Press F12 in browser

# Ollama logs
# Check console output
```

---

## 🎯 Success Indicators

### **System Healthy When:**
- ✅ All health endpoints return 200
- ✅ Ollama models available
- ✅ LLM direct calls work
- ✅ No port conflicts

### **Generation Working When:**
- ✅ Backend accepts requests
- ✅ AI Core processes requests
- ✅ CrewAI executes successfully
- ✅ Files are generated

---

## 📚 Documentation Links

- [Debugging Guide](./GENESIS_DEBUGGING_GUIDE.md)
- [Technical Architecture](./TECHNICAL_ARCHITECTURE.md)
- [Troubleshooting Guide](./TROUBLESHOOTING_GUIDE.md)
- [Setup Guide](./GENESIS_SETUP_GUIDE.txt)

---

## 🆘 Quick Help

**If something's not working:**

1. **Run health check** - See if services are running
2. **Check logs** - Look for error messages
3. **Restart services** - In correct order: Ollama → AI Core → Backend → Frontend
4. **Check ports** - Make sure no conflicts
5. **Check dependencies** - Ensure all packages installed

**Remember**: Most issues can be resolved by restarting services in the correct order! 🚀 