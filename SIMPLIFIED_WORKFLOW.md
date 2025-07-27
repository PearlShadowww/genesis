# Genesis Simplified Workflow

This document describes the simplified Genesis workflow for testing prompt-to-generation functionality.

## Overview

The Genesis system has been simplified to focus on the core functionality:
- **Frontend**: Simple text area for entering prompts
- **Backend**: Rust API that coordinates the generation process
- **AI Core**: Python service that interfaces with Ollama LLM
- **Ollama**: Local LLM for generating code files

## Architecture

```
Frontend (React) → Backend (Rust) → AI Core (Python) → Ollama (LLM)
     ↓                ↓                ↓                ↓
  Text Area    Project Management   File Generation   Code Creation
```

## Components

### 1. Frontend (`genesis-frontend/`)
- **Technology**: React + TypeScript + Chakra UI
- **Port**: 1420 (Tauri) or 3000 (Web)
- **Features**:
  - Text area for project prompts
  - Real-time generation status
  - Project history sidebar
  - File preview and download
  - Connection status monitoring

### 2. Backend (`backend/`)
- **Technology**: Rust + Actix Web + MongoDB
- **Port**: 8080
- **Features**:
  - Project generation coordination
  - MongoDB storage for project history
  - Health monitoring for all services
  - RESTful API endpoints

### 3. AI Core (`ai_core/`)
- **Technology**: Python + FastAPI
- **Port**: 8000
- **Features**:
  - Direct Ollama integration
  - File generation from prompts
  - Project manifest creation
  - Error handling and fallbacks

### 4. Ollama
- **Port**: 11434
- **Model**: llama3.1:8b (default)
- **Features**:
  - Local LLM inference
  - Code generation capabilities
  - HTTP API interface

## Quick Start

### 1. Start All Services

```bash
# Terminal 1: Start Backend
cd backend
cargo run

# Terminal 2: Start AI Core
cd ai_core
python main.py

# Terminal 3: Start Frontend
cd genesis-frontend
npm run tauri dev
```

### 2. Test the Workflow

```bash
# Run the test script
python test_simple_workflow.py
```

### 3. Use the Frontend

1. Open the frontend application
2. Enter a project description in the text area
3. Click "Generate Project"
4. Monitor the generation progress in the terminal output
5. View generated files and download them

## API Endpoints

### Backend (Port 8080)
- `GET /health` - Health check
- `POST /generate` - Start project generation
- `GET /projects` - List all projects
- `GET /projects/{id}` - Get project details

### AI Core (Port 8000)
- `GET /health` - Health check
- `POST /run` - Generate project files

### Ollama (Port 11434)
- `POST /api/generate` - Generate text with LLM

## Example Usage

### Frontend Prompt
```
Create a React todo app with add, delete, and mark complete functionality
```

### Generated Files
- `package.json` - Project configuration
- `src/App.tsx` - Main React component
- `README.md` - Project documentation

## Testing

The `test_simple_workflow.py` script tests:
1. Backend connectivity
2. AI Core connectivity
3. Ollama connectivity
4. Complete project generation workflow

## Troubleshooting

### Common Issues

1. **Backend not connecting**
   - Ensure MongoDB is running
   - Check port 8080 is available

2. **AI Core not responding**
   - Verify Python dependencies are installed
   - Check port 8000 is available

3. **Ollama not working**
   - Ensure Ollama is installed and running
   - Verify model `llama3.1:8b` is downloaded

4. **Frontend connection issues**
   - Check all backend services are running
   - Verify CORS settings

### Health Checks

```bash
# Test backend
curl http://127.0.0.1:8080/health

# Test AI core
curl http://127.0.0.1:8000/health

# Test Ollama
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.1:8b","prompt":"Hello","stream":false}'
```

## Next Steps

This simplified version focuses on core functionality. Future enhancements could include:
- Advanced project templates
- Multiple LLM support
- Project structure customization
- Real-time collaboration
- Advanced UI components
- Deployment automation 