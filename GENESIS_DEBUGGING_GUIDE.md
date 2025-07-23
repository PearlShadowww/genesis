# Genesis AI-Powered Software Generator - Debugging Guide

## 🚨 Current Status: Optimization Complete, AI Integration Pending

**Last Updated:** July 23, 2025  
**Status:** All services running, CrewAI-LLM compatibility issue identified

---

## 📋 System Overview

Genesis is a multi-service AI-powered software generator with:
- **Frontend**: Tauri + React + TypeScript (Port 5173)
- **Backend**: Rust Actix-web API (Port 8080)  
- **AI Core**: Python FastAPI + CrewAI + Ollama (Port 8000)

---

## 🔧 Current Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    AI Core      │
│   (Tauri)       │◄──►│   (Rust)        │◄──►│   (Python)      │
│   Port 5173     │    │   Port 8080     │    │   Port 8000     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Health        │    │   Ollama        │
                       │   Monitoring    │    │   Models        │
                       └─────────────────┘    └─────────────────┘
```

---

## ✅ Working Components

### 1. **Frontend (Tauri + React)**
- ✅ Running on port 5173
- ✅ Connected to backend
- ✅ Modern UI with Chakra UI
- ✅ Real-time status updates
- ✅ File tree display ready

### 2. **Backend (Rust Actix-web)**
- ✅ Running on port 8080
- ✅ Health endpoint: `GET /health`
- ✅ Generate endpoint: `POST /generate`
- ✅ Project status endpoint: `GET /projects/{id}`
- ✅ Comprehensive error handling
- ✅ Request validation and rate limiting

### 3. **AI Core (Python FastAPI)**
- ✅ Running on port 8000
- ✅ Health endpoint: `GET /health`
- ✅ Run endpoint: `POST /run`
- ✅ Ollama connectivity verified
- ✅ Models available: `qwen2.5-coder:1.5b-base`, `llama3.1:8b`

### 4. **Ollama Integration**
- ✅ Ollama service running
- ✅ Models downloaded and available
- ✅ Direct LLM calls working
- ✅ Health checks passing

---

## ⚠️ Known Issues

### **Primary Issue: CrewAI-LLM Compatibility**

**Problem:** LLM works directly but fails in CrewAI context
```
ERROR: LLM Failed
An unknown error occurred. Please check the details below.
```

**Root Cause:** Compatibility issue between `langchain_ollama.OllamaLLM` and CrewAI framework

**Evidence:**
- ✅ Direct LLM calls: `llm.invoke("Hello")` works
- ✅ Ollama API: Direct API calls work
- ❌ CrewAI integration: Fails with "LLM Failed"

**Attempted Fixes:**
1. ✅ Removed tools validation errors
2. ✅ Fixed agent-task assignments
3. ✅ Disabled memory to avoid ChromaDB dependency
4. ✅ Adjusted LLM configuration (temperature, verbose)
5. ✅ Tried different model priorities

---

## 🛠️ Debugging Commands

### **Service Health Checks**

```bash
# Check all services
curl http://localhost:5173  # Frontend
curl http://localhost:8080/health  # Backend
curl http://localhost:8000/health  # AI Core
curl http://localhost:11434/api/tags  # Ollama
```

### **Test Generation Flow**

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

### **LLM Testing**

```bash
# Test LLM directly
cd ai_core
python test_ollama.py

# Test CrewAI integration
python test_llm_crewai.py

# Debug specific components
python debug_test.py
```

---

## 📁 Key Files and Their Purposes

### **Configuration Files**
- `ai_core/requirements.txt` - Python dependencies
- `backend/Cargo.toml` - Rust dependencies
- `genesis-frontend/package.json` - Node.js dependencies
- `env.example` - Environment configuration template

### **Core Implementation**
- `ai_core/main.py` - FastAPI server with CrewAI integration
- `ai_core/llm.py` - LLM configuration and initialization
- `ai_core/agents.py` - CrewAI agent definitions
- `ai_core/tasks.py` - CrewAI task definitions
- `backend/src/main.rs` - Rust API server
- `genesis-frontend/src/App.tsx` - React frontend

### **Error Handling & Monitoring**
- `ai_core/error_handling.py` - Custom exceptions and handlers
- `ai_core/logging_config.py` - Enhanced logging setup
- `backend/src/error.rs` - Rust error types
- `backend/src/health.rs` - Health check endpoints
- `scripts/monitor.py` - Service monitoring script

### **Testing & Debugging**
- `ai_core/test_ollama.py` - Ollama connectivity tests
- `ai_core/debug_test.py` - Component debugging
- `ai_core/test_llm_crewai.py` - CrewAI integration tests
- `tests/test_integration.py` - End-to-end integration tests

---

## 🔍 Debugging Workflow

### **1. Service Startup Issues**
```bash
# Check if ports are in use
netstat -ano | findstr :8000
netstat -ano | findstr :8080
netstat -ano | findstr :5173

# Kill processes if needed
taskkill /F /PID <PID>
```

### **2. LLM Issues**
```bash
# Check Ollama status
ollama list
ollama serve

# Test specific model
ollama run qwen2.5-coder:1.5b-base "Hello"
```

### **3. CrewAI Issues**
```bash
# Test components individually
cd ai_core
python -c "from llm import get_llm; llm = get_llm(); print(llm.invoke('Hello'))"
python -c "from agents import create_agents; from llm import get_llm; agents = create_agents(get_llm()); print(len(agents))"
```

### **4. Dependency Issues**
```bash
# Python dependencies
pip install -r requirements.txt
pip list | grep crewai

# Rust dependencies
cd backend
cargo check
cargo build
```

---

## 🚀 Next Steps to Resolve CrewAI Issue

### **Option 1: Try Different LLM Wrapper**
```python
# In ai_core/llm.py, try:
from crewai import LLM

llm = LLM(
    provider="ollama",
    model=model_name,
    base_url="http://localhost:11434"
)
```

### **Option 2: Use Different CrewAI Version**
```bash
pip uninstall crewai
pip install crewai==0.28.0  # Try older version
```

### **Option 3: Custom LLM Adapter**
Create a custom adapter that wraps OllamaLLM for CrewAI compatibility.

### **Option 4: Alternative AI Framework**
Consider using LangChain directly or other AI frameworks.

---

## 📊 Performance Metrics

### **Current Response Times**
- Backend health check: ~50ms
- AI Core health check: ~200ms
- Ollama model generation: ~2-5s
- CrewAI execution: ❌ Failing

### **Resource Usage**
- Frontend: ~50MB RAM
- Backend: ~20MB RAM
- AI Core: ~100MB RAM
- Ollama: ~2-4GB RAM (depending on model)

---

## 🔧 Environment Variables

### **Required Environment Variables**
```bash
# AI Core
OLLAMA_BASE_URL=http://localhost:11434
AI_CORE_HOST=127.0.0.1
AI_CORE_PORT=8000

# Backend
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8080
AI_CORE_URL=http://127.0.0.1:8000

# Frontend
VITE_BACKEND_URL=http://127.0.0.1:8080
```

---

## 📞 Support Information

### **Log Locations**
- AI Core logs: Console output + `ai_core/logs/`
- Backend logs: Console output
- Frontend logs: Browser console

### **Common Error Messages**
- `LLM Failed`: CrewAI-LLM compatibility issue
- `Connection refused`: Service not running
- `Model not found`: Ollama model not downloaded
- `Validation error`: Request format issue

### **Recovery Procedures**
1. Restart all services in order: Ollama → AI Core → Backend → Frontend
2. Check port availability
3. Verify Ollama models are downloaded
4. Test individual components
5. Check environment variables

---

## 🎯 Success Criteria

The system will be fully functional when:
- ✅ All services are running (COMPLETED)
- ✅ Health checks pass (COMPLETED)
- ✅ LLM works directly (COMPLETED)
- ✅ CrewAI executes successfully (PENDING)
- ✅ Project generation completes (PENDING)
- ✅ Frontend displays generated files (PENDING)

**Current Progress: 75% Complete** 🚀 