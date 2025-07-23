# Genesis Troubleshooting Guide

## 🚨 Quick Diagnosis

### **Service Status Check**
```bash
# Check all services in one command
curl -s http://localhost:5173 > /dev/null && echo "✅ Frontend" || echo "❌ Frontend"
curl -s http://localhost:8080/health > /dev/null && echo "✅ Backend" || echo "❌ Backend"
curl -s http://localhost:8000/health > /dev/null && echo "✅ AI Core" || echo "❌ AI Core"
curl -s http://localhost:11434/api/tags > /dev/null && echo "✅ Ollama" || echo "❌ Ollama"
```

---

## 🔧 Common Issues & Solutions

### **1. Service Won't Start**

#### **Port Already in Use**
```bash
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8080
netstat -ano | findstr :5173

# Kill the process
taskkill /F /PID <PID>
```

#### **Permission Issues**
```bash
# Run as administrator (Windows)
# Or check file permissions (Linux/Mac)
ls -la ai_core/
chmod +x ai_core/main.py
```

#### **Missing Dependencies**
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

---

### **2. Ollama Issues**

#### **Ollama Not Running**
```bash
# Start Ollama
ollama serve

# Check if it's running
curl http://localhost:11434/api/tags
```

#### **Models Not Found**
```bash
# List available models
ollama list

# Pull required models
ollama pull qwen2.5-coder:1.5b-base
ollama pull llama3.1:8b

# Test a model
ollama run qwen2.5-coder:1.5b-base "Hello"
```

#### **Model Generation Fails**
```bash
# Check model status
ollama show qwen2.5-coder:1.5b-base

# Restart Ollama
ollama serve

# Try different model
# Edit ai_core/llm.py to use different model
```

---

### **3. AI Core Issues**

#### **CrewAI-LLM Compatibility Error**
```
ERROR: LLM Failed
An unknown error occurred.
```

**Solutions:**
1. **Try different LLM wrapper:**
   ```python
   # In ai_core/llm.py
   from crewai import LLM
   
   llm = LLM(
       provider="ollama",
       model=model_name,
       base_url="http://localhost:11434"
   )
   ```

2. **Try different CrewAI version:**
   ```bash
   pip uninstall crewai
   pip install crewai==0.28.0
   ```

3. **Use simpler configuration:**
   ```python
   # In ai_core/llm.py
   llm = OllamaLLM(
       model=model_name,
       base_url="http://localhost:11434",
       temperature=0.1,
       verbose=False
   )
   ```

#### **Import Errors**
```bash
# Check Python environment
python --version
pip list | grep crewai
pip list | grep langchain

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### **Memory/ChromaDB Error**
```
The CHROMA_OPENAI_API_KEY environment variable is not set.
```

**Solution:**
```python
# In ai_core/main.py, disable memory
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,
    memory=False  # Disable memory
)
```

---

### **4. Backend Issues**

#### **Compilation Errors**
```bash
cd backend
cargo check
cargo build

# Check Rust version
rustc --version
cargo --version
```

#### **Connection Refused**
```bash
# Check if backend is running
curl http://localhost:8080/health

# Check logs
# Backend logs are in console output
```

#### **Validation Errors**
```bash
# Test with valid request
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test","backend":"ollama"}'
```

---

### **5. Frontend Issues**

#### **Build Errors**
```bash
cd genesis-frontend
npm install
npm run build
```

#### **Connection Issues**
```bash
# Check if backend is accessible
curl http://localhost:8080/health

# Check frontend configuration
# Look for VITE_BACKEND_URL in .env
```

#### **Tauri Issues**
```bash
# Check Tauri dependencies
npm list @tauri-apps/api

# Rebuild Tauri
npm run tauri build
```

---

## 🔍 Debugging Commands

### **Comprehensive Health Check**
```bash
#!/bin/bash
echo "🔍 Genesis Health Check"
echo "========================"

# Check services
echo "📡 Checking services..."
curl -s http://localhost:5173 > /dev/null && echo "✅ Frontend (5173)" || echo "❌ Frontend (5173)"
curl -s http://localhost:8080/health > /dev/null && echo "✅ Backend (8080)" || echo "❌ Backend (8080)"
curl -s http://localhost:8000/health > /dev/null && echo "✅ AI Core (8000)" || echo "❌ AI Core (8000)"
curl -s http://localhost:11434/api/tags > /dev/null && echo "✅ Ollama (11434)" || echo "❌ Ollama (11434)"

# Check models
echo "🤖 Checking Ollama models..."
ollama list

# Check processes
echo "🔄 Checking processes..."
netstat -ano | findstr :8000
netstat -ano | findstr :8080
netstat -ano | findstr :5173
```

### **Test Generation Flow**
```bash
# Test backend generation
echo "🧪 Testing backend generation..."
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Create a simple React counter","backend":"ollama"}' \
  -w "\nStatus: %{http_code}\nTime: %{time_total}s\n"

# Test AI core directly
echo "🧪 Testing AI core directly..."
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Create a simple React counter","backend":"ollama"}' \
  -w "\nStatus: %{http_code}\nTime: %{time_total}s\n"
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

## 📊 Error Code Reference

### **HTTP Status Codes**
- `200`: Success
- `400`: Bad Request (validation error)
- `404`: Not Found
- `500`: Internal Server Error
- `503`: Service Unavailable

### **Common Error Messages**

#### **Backend Errors**
```
{"success":false,"message":"Validation error","data":null}
```
- **Cause**: Invalid request format
- **Solution**: Check request JSON structure

```
{"success":false,"message":"AI core error","data":null}
```
- **Cause**: AI Core service issue
- **Solution**: Check AI Core logs and status

#### **AI Core Errors**
```
"LLM Failed"
```
- **Cause**: CrewAI-LLM compatibility issue
- **Solution**: See CrewAI-LLM Compatibility section

```
"Connection refused"
```
- **Cause**: Ollama not running
- **Solution**: Start Ollama service

#### **Frontend Errors**
```
"Failed to fetch"
```
- **Cause**: Backend not accessible
- **Solution**: Check backend service and URL

```
"Backend disconnected"
```
- **Cause**: Backend service down
- **Solution**: Restart backend service

---

## 🛠️ Recovery Procedures

### **Complete System Reset**
```bash
# 1. Stop all services
taskkill /F /IM python.exe
taskkill /F /IM node.exe
taskkill /F /IM ollama.exe

# 2. Clear ports
netstat -ano | findstr :8000 | awk '{print $5}' | xargs taskkill /F /PID
netstat -ano | findstr :8080 | awk '{print $5}' | xargs taskkill /F /PID
netstat -ano | findstr :5173 | awk '{print $5}' | xargs taskkill /F /PID

# 3. Start services in order
ollama serve
cd ai_core && python main.py &
cd backend && cargo run &
cd genesis-frontend && npm run tauri dev &
```

### **Service-Specific Recovery**

#### **AI Core Recovery**
```bash
cd ai_core
# Clear Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Restart service
python main.py
```

#### **Backend Recovery**
```bash
cd backend
# Clean build
cargo clean
cargo build

# Restart service
cargo run
```

#### **Frontend Recovery**
```bash
cd genesis-frontend
# Clear node modules
rm -rf node_modules
npm install

# Restart service
npm run tauri dev
```

---

## 📞 Support Information

### **Log Locations**
- **AI Core**: Console output + `ai_core/logs/`
- **Backend**: Console output
- **Frontend**: Browser console (F12)
- **Ollama**: Console output

### **Useful Commands**
```bash
# Check system resources
top
htop
tasklist

# Check network connections
netstat -an
netstat -ano | findstr :8000

# Check disk space
df -h
dir

# Check memory usage
free -h
wmic OS get FreePhysicalMemory
```

### **Environment Variables**
```bash
# Check environment
echo $AI_CORE_URL
echo $BACKEND_URL
echo $OLLAMA_URL

# Set environment variables
export AI_CORE_URL=http://127.0.0.1:8000
export BACKEND_URL=http://127.0.0.1:8080
export OLLAMA_URL=http://localhost:11434
```

---

## 🎯 Success Indicators

### **System is Healthy When:**
- ✅ All health endpoints return 200
- ✅ Ollama models are available
- ✅ LLM direct calls work
- ✅ Services start without errors
- ✅ No port conflicts
- ✅ All dependencies installed

### **Generation is Working When:**
- ✅ Backend accepts generation requests
- ✅ AI Core processes requests
- ✅ CrewAI executes successfully
- ✅ Files are generated
- ✅ Frontend displays results

---

## 🔮 Advanced Debugging

### **Enable Verbose Logging**
```python
# In ai_core/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Profile Performance**
```bash
# Python profiling
python -m cProfile -o profile.stats ai_core/main.py

# Rust profiling
cargo build --release
perf record cargo run
```

### **Network Debugging**
```bash
# Monitor network traffic
tcpdump -i lo0 port 8000
tcpdump -i lo0 port 8080
```

---

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Actix-web Documentation](https://actix.rs/)
- [Tauri Documentation](https://tauri.app/docs)

---

## 🆘 Emergency Contacts

If you're still experiencing issues:

1. **Check the logs** for specific error messages
2. **Run the health check script** to identify failing components
3. **Review this troubleshooting guide** for your specific error
4. **Try the recovery procedures** for your service
5. **Check the debugging guide** for detailed analysis

**Remember**: Most issues can be resolved by restarting services in the correct order: Ollama → AI Core → Backend → Frontend 