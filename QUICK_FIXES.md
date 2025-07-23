# Genesis Quick Fixes

## 🚨 Emergency Fixes

### Service Won't Start
```bash
# Stop everything
./stop_all.sh

# Clear ports
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:8080 | xargs kill -9
sudo lsof -ti:1420 | xargs kill -9

# Restart
./start_all.sh
```

### Ollama Issues
```bash
# Restart Ollama
pkill ollama
ollama serve

# Check models
ollama list

# Pull missing model
ollama pull qwen2.5-coder:1.5b-base
```

### Python Dependencies
```bash
cd ai_core
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Rust Build Issues
```bash
cd backend
rustup update
cargo clean
cargo build
```

### Node.js Issues
```bash
cd genesis-frontend
rm -rf node_modules package-lock.json
npm install
```

## �� Common Solutions

| Problem | Quick Fix |
|---------|-----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Connection refused | `ollama serve` |
| Model not found | `ollama pull qwen2.5-coder:1.5b-base` |
| CORS errors | Check CORS config in backend |
| Port conflicts | Kill processes using ports 8000, 8080, 1420 |
| Memory issues | Use smaller models (phi3:mini) |
| Slow generation | Lower temperature to 0.3 |

## 📞 Get Help

1. Run diagnostics: `./test_all.sh`
2. Check logs: `tail -f logs/*.log`
3. Report issue with system info and error messages 