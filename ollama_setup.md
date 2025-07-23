🧪 Genesis AI Core Test Suite
======================

# Ollama Setup Guide for Genesis

This guide provides detailed instructions for setting up Ollama as the local LLM backend for the Genesis AI-powered software generator.

## What is Ollama?

Ollama is an open-source tool that allows you to run large language models locally on your machine. It provides a simple API for interacting with various models and is perfect for the Genesis project's local AI processing requirements.

## Prerequisites

- Windows 10/11, macOS, or Linux
- At least 8GB RAM (16GB recommended)
- 10GB free disk space
- Internet connection for downloading models

## Installation

### Windows
1. Download Ollama from https://ollama.ai/
2. Run the installer and follow the setup wizard
3. Ollama will be installed as a Windows service

### macOS
```bash
# Using Homebrew
brew install ollama

# Or download from https://ollama.ai/
```

### Linux
```bash
# Using curl
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai/
```

## Starting Ollama

### Windows
Ollama runs automatically as a Windows service. To start manually:
```cmd
ollama serve
```

### macOS/Linux
```bash
ollama serve
```

## Downloading Required Models

Genesis requires specific models for optimal performance. Download them using these commands:

```bash
# Primary coding model (recommended)
ollama pull qwen2.5-coder:1.5b-base

# Alternative coding model
ollama pull codellama:7b

# General purpose model for planning
ollama pull llama3.1:8b

# Fast model for simple tasks
ollama pull phi3:mini
```

## Model Information

### qwen2.5-coder:1.5b-base
- **Size**: ~1.5GB
- **Purpose**: Primary code generation
- **Strengths**: Excellent at coding tasks, fast inference
- **Use Case**: Main coding agent

### codellama:7b
- **Size**: ~4GB
- **Purpose**: Alternative code generation
- **Strengths**: Very good at coding, larger context
- **Use Case**: Backup coding agent

### llama3.1:8b
- **Size**: ~5GB
- **Purpose**: General planning and reasoning
- **Strengths**: Good reasoning, planning capabilities
- **Use Case**: Planning agent

### phi3:mini
- **Size**: ~1.5GB
- **Purpose**: Fast simple tasks
- **Strengths**: Very fast, good for simple operations
- **Use Case**: Quick validations and simple tasks

## Testing Ollama Installation

### Check if Ollama is running
```bash
curl http://localhost:11434/api/tags
```

Expected response:
```json
{
  "models": [
    {
      "name": "qwen2.5-coder:1.5b-base",
      "size": 1572864000,
      "modified_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Test basic generation
```bash
ollama run qwen2.5-coder:1.5b-base "Write a simple JavaScript function"
```

### Test API endpoint
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder:1.5b-base",
    "prompt": "Write a hello world function in JavaScript"
  }'
```

## Configuration

### Environment Variables
Create a `.env` file in the `ai_core` directory:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:1.5b-base
OLLAMA_TIMEOUT=120
OLLAMA_TEMPERATURE=0.7
```

### Model Configuration
You can customize model parameters in the AI core:

```python
# In ai_core/llm.py
llm = OllamaLLM(
    model="qwen2.5-coder:1.5b-base",
    base_url="http://localhost:11434",
    temperature=0.7,  # Lower for more focused code generation
    timeout=120,
    verbose=True
)
```

## Performance Optimization

### Hardware Recommendations
- **CPU**: Modern multi-core processor
- **RAM**: 16GB minimum, 32GB recommended
- **Storage**: SSD for faster model loading
- **GPU**: Optional, but significantly improves performance

### Memory Management
```bash
# Check model memory usage
ollama list

# Remove unused models to free space
ollama rm unused-model-name
```

### GPU Acceleration (Optional)
If you have a compatible GPU:

```bash
# Install CUDA version (if available)
# Models will automatically use GPU if detected
```

## Troubleshooting

### Common Issues

#### 1. "Connection refused" error
```bash
# Check if Ollama is running
ollama serve

# Check if port 11434 is available
netstat -an | grep 11434
```

#### 2. "Model not found" error
```bash
# List available models
ollama list

# Pull the required model
ollama pull qwen2.5-coder:1.5b-base
```

#### 3. "Out of memory" error
```bash
# Check available memory
free -h  # Linux
systeminfo | findstr "Total Physical Memory"  # Windows

# Use smaller models or increase swap space
```

#### 4. Slow performance
- Ensure you have sufficient RAM
- Close other memory-intensive applications
- Consider using a smaller model for testing
- Check if GPU acceleration is working

### Logs and Debugging

#### Enable verbose logging
```bash
ollama serve --verbose
```

#### Check Ollama logs
```bash
# Windows
# Check Event Viewer for Ollama service logs

# macOS/Linux
journalctl -u ollama -f
```

#### Test with different models
```bash
# Try a smaller model for testing
ollama pull phi3:mini
ollama run phi3:mini "Hello world"
```

## Integration with Genesis

### Testing Integration
Run the Genesis test suite:

```bash
cd ai_core
python test_ollama.py
```

### Expected Test Results 