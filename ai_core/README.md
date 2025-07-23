# Genesis AI Core

Python FastAPI server with CrewAI multi-agent system for intelligent software generation.

## Features
- CrewAI agents for planning, coding, and debugging
- Ollama integration for local LLM processing
- Project structure generation
- Code validation and error fixing

## Setup
```bash
cd ai_core
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

## Dependencies
- FastAPI
- CrewAI
- Ollama
- Pydantic
- Uvicorn 