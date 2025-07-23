# Genesis Troubleshooting Guide

This guide provides solutions to common issues encountered when setting up and running Genesis.

## �� Quick Diagnostic

Run the diagnostic script to identify issues:
```bash
# Windows
validate_genesis.ps1

# Linux/macOS
./test_all.sh
```

## �� Python Issues

### ModuleNotFoundError: No module named 'langchain_ollama'

**Problem**: Missing Python dependencies

**Solution**:
```bash
cd ai_core
pip install langchain-ollama
# Or reinstall all dependencies
pip install -r requirements.txt
```

**Prevention**: Always activate the virtual environment before running Python scripts.

### ImportError: cannot import name 'CrewAI'

**Problem**: CrewAI not installed or wrong version

**Solution**:
```bash
pip uninstall crewai
pip install crewai==0.28.0
```

**Alternative**: Use a different CrewAI version if available:
```bash
pip install crewai==0.27.0
```

### PermissionError: [Errno 13] Permission denied

**Problem**: File permission issues

**Solution**:
```bash
# Linux/macOS
chmod +x *.sh
chmod +x ai_core/*.py

# Windows
# Run PowerShell as Administrator
```

## �� Ollama Issues

### Connection refused: localhost:11434

**Problem**: Ollama is not running

**Solution**:
```bash
# Start Ollama
ollama serve

# Check if it's running
curl http://localhost:11434/api/tags
```

**Alternative**: Check if Ollama is installed:
```bash
# Windows
ollama --version

# Linux/macOS
which ollama
```

### Model not found: qwen2.5-coder:1.5b-base

**Problem**: Required model not downloaded

**Solution**:
```bash
# Download the model
ollama pull qwen2.5-coder:1.5b-base

# Check available models
ollama list
```

**Alternative**: Use a different model:
```bash
# Edit ai_core/llm.py
llm = OllamaLLM(
    model="llama3.1:8b",  # Use available model
    base_url="http://localhost:11434",
    temperature=0.7,
    timeout=120,
    verbose=True
)
```

### Out of memory error

**Problem**: Insufficient RAM for model

**Solution**:
```bash
# Use smaller model
ollama pull phi3:mini

# Or increase swap space (Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 🦀 Rust Issues

### error: failed to run custom build command

**Problem**: Missing system dependencies

**Solution**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install build-essential pkg-config libssl-dev

# macOS
xcode-select --install

# Windows
# Install Visual Studio Build Tools
```

### error: linking with `cc` failed

**Problem**: Compiler issues

**Solution**:
```bash
# Update Rust toolchain
rustup update

# Clean and rebuild
cargo clean
cargo build
```

### cannot find -lssl

**Problem**: OpenSSL library missing

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install libssl-dev

# macOS
brew install openssl

# Windows
# Install vcpkg or use pre-built binaries
```

## 🟢 Node.js Issues

### npm ERR! code ETARGET

**Problem**: Package version not found

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Update npm
npm install -g npm@latest

# Try alternative package
# Edit package.json to use available version
```

### EACCES: permission denied

**Problem**: Permission issues

**Solution**:
```bash
# Fix npm permissions
sudo chown -R $USER:$GROUP ~/.npm
sudo chown -R $USER:$GROUP ~/.config

# Or use nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
nvm use node
```

### Module not found: tree-sitter-dart

**Problem**: Non-existent package

**Solution**:
```bash
# Remove non-existent package from package.json
npm uninstall tree-sitter-dart

# Or use alternative Dart parser
npm install tree-sitter-dart-sdk
```

## 🌐 Network Issues

### Connection refused errors

**Problem**: Services not running on expected ports

**Solution**:
```bash
# Check what's using the ports
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :8080

# Linux/macOS
lsof -i :8000
lsof -i :8080

# Kill conflicting processes
kill -9 <PID>
```

### CORS errors in browser

**Problem**: Cross-origin requests blocked

**Solution**:
```bash
# Check CORS configuration in backend/src/main.rs
# Ensure allowed_origins includes your frontend URL
```

**Alternative**: Use browser with disabled security (development only):
```bash
# Chrome
chrome --disable-web-security --user-data-dir=/tmp/chrome_dev

# Firefox
firefox --disable-web-security
```

## 🔧 Service Startup Issues

### AI Core won't start

**Problem**: Various startup issues

**Solution**:
```bash
# Check Python version
python --version  # Should be 3.8+

# Check virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Check dependencies
pip list | grep fastapi
pip list | grep crewai

# Check logs
tail -f genesis.log
```

### Rust Backend compilation fails

**Problem**: Build errors

**Solution**:
```bash
# Update Rust
rustup update

# Clean build
cargo clean
cargo build --verbose

# Check for specific errors in output
```

### Tauri frontend build fails

**Problem**: Frontend compilation issues

**Solution**:
```bash
# Check Node.js version
node --version  # Should be 18+

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npm run type-check
```

## 🐛 Runtime Issues

### CrewAI agents not generating proper output

**Problem**: Poor quality or no output from AI agents

**Solution**:
```bash
# Simplify agent prompts for local models
# Edit ai_core/agents.py - reduce complexity

# Lower temperature for more focused output
# Edit ai_core/llm.py
llm = OllamaLLM(
    model="qwen2.5-coder:1.5b-base",
    temperature=0.3,  # Lower temperature
    timeout=120,
    verbose=True
)

# Use smaller models for faster responses
ollama pull phi3:mini
```

### Slow generation times

**Problem**: Generation taking too long

**Solution**:
```bash
# Use smaller models
ollama pull phi3:mini
ollama pull qwen2.5-coder:1.5b-base

# Increase system resources
# Close other applications
# Add more RAM if possible

# Optimize prompts
# Make prompts more specific and concise
```

### Memory leaks or high resource usage

**Problem**: System resources exhausted

**Solution**:
```bash
# Monitor resource usage
htop  # Linux/macOS
taskmgr  # Windows

# Restart services periodically
./stop_all.sh
./start_all.sh

# Use resource limits
# Edit startup scripts to limit memory usage
```

## 🔍 Debugging Techniques

### Enable verbose logging

**Python (AI Core)**:
```python
# Edit ai_core/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Rust (Backend)**:
```bash
# Set environment variable
export RUST_LOG=debug
cargo run
```

**Node.js (Frontend)**:
```bash
# Enable debug logging
DEBUG=* npm run tauri dev
```

### Check service health

```bash
# AI Core
curl http://127.0.0.1:8000/health

# Rust Backend
curl http://127.0.0.1:8080/health

# Ollama
curl http://localhost:11434/api/tags
```

### Monitor logs

```bash
# Follow logs in real-time
tail -f ai_core/genesis.log
tail -f logs/backend.log

# Search for errors
grep -i error genesis.log
grep -i exception genesis.log
```

## 🆘 Getting Help

### Before asking for help

1. **Run diagnostic scripts**
   ```bash
   ./test_all.sh
   python ai_core/test_ollama.py
   ```

2. **Check logs for errors**
   ```bash
   tail -n 50 genesis.log
   ```

3. **Verify system requirements**
   ```bash
   python --version
   node --version
   rustc --version
   ollama --version
   ```

4. **Try minimal reproduction**
   - Test with simple prompts
   - Use default configurations
   - Test individual components

### Where to get help

- **GitHub Issues**: [Report bugs](https://github.com/genesis-ai/genesis/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/genesis-ai/genesis/discussions)
- **Documentation**: [Wiki](https://github.com/genesis-ai/genesis/wiki)
- **Community**: [Discord/Slack](https://discord.gg/genesis)

### Information to include

When reporting issues, include:

1. **System information**
   ```bash
   # OS and version
   uname -a  # Linux/macOS
   systeminfo  # Windows
   
   # Component versions
   python --version
   node --version
   rustc --version
   ollama --version
   ```

2. **Error messages**
   - Full error output
   - Stack traces
   - Log files

3. **Steps to reproduce**
   - Exact commands run
   - Input provided
   - Expected vs actual behavior

4. **Environment details**
   - Virtual environment status
   - Network configuration
   - Resource usage

## 🔄 Recovery Procedures

### Complete reset

```bash
# Stop all services
./stop_all.sh

# Clean build artifacts
cd backend && cargo clean
cd ../genesis-frontend && rm -rf node_modules dist
cd ../ai_core && rm -rf __pycache__ *.pyc

# Reinstall dependencies
cd ../ai_core && pip install -r requirements.txt
cd ../backend && cargo build
cd ../genesis-frontend && npm install
cd ../tree_sitter && npm install

# Restart services
./start_all.sh
```

### Database/state reset

```bash
# Clear generated projects
rm -rf ai_core/projects/*

# Clear logs
rm -rf logs/*
rm -f ai_core/genesis.log

# Reset Ollama (if needed)
ollama rm qwen2.5-coder:1.5b-base
ollama pull qwen2.5-coder:1.5b-base
```

---

For additional help, check the [FAQ](FAQ.md) or [Wiki](https://github.com/genesis-ai/genesis/wiki). 