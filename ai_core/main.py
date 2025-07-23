from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging
import json
import os
from datetime import datetime
from pathlib import Path

# Performance optimizations
try:
    import orjson
    JSON_LIB = orjson
except ImportError:
    JSON_LIB = json

# Platform-specific optimizations
import platform
if platform.system() != "Windows":
    try:
        import uvloop
        import asyncio
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

# Import our modules
from models import Prompt, ProjectResponse
from agents import create_agents
from tasks import create_tasks
from llm import get_llm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Genesis AI Core",
    description="AI-powered software generator using CrewAI and Ollama",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Genesis AI Core is running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate": "/run"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Ollama connectivity
        llm = get_llm()
        response = llm.invoke("Hello")
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "ollama": "connected",
                "crewai": "ready"
            },
            "message": "All services are operational"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

@app.post("/run")
async def run_crew(prompt_data: Prompt):
    """Main endpoint for project generation"""
    try:
        logger.info(f"Starting project generation for prompt: {prompt_data.prompt[:100]}...")
        
        # Create project ID
        project_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = PROJECTS_DIR / project_id
        project_dir.mkdir(exist_ok=True)
        
        # Initialize LLM
        llm = get_llm()
        
        # Create agents
        agents = create_agents(llm)
        
        # Create tasks
        tasks = create_tasks(prompt_data.prompt)
        
        # Assign agents to tasks
        tasks[0].agent = agents[0]  # Planner task -> Planner agent
        tasks[1].agent = agents[1]  # Code task -> Coder agent
        tasks[2].agent = agents[2]  # Debug task -> Debugger agent
        
        # Create crew
        from crewai import Crew
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            memory=False
        )
        
        logger.info("Starting CrewAI workflow...")
        
        # Run the crew
        result = crew.kickoff()
        
        logger.info("CrewAI workflow completed")
        
        # Parse the result
        project_response = parse_crew_result(result, prompt_data.prompt)
        
        # Save project manifest
        save_project_manifest(project_id, prompt_data, project_response)
        
        logger.info(f"Project {project_id} generated successfully")
        
        return project_response
        
    except Exception as e:
        logger.error(f"Project generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Project generation failed: {str(e)}"
        )

def parse_crew_result(result, original_prompt: str) -> ProjectResponse:
    """Parse CrewAI result into structured response"""
    try:
        # Extract files from result
        files = []
        
        # Look for file content in the result
        result_text = str(result)
        
        # Simple parsing - look for code blocks
        import re
        
        # Pattern to match code blocks with language and filename
        code_pattern = r'```(\w+):([^\n]+)\n(.*?)```'
        matches = re.findall(code_pattern, result_text, re.DOTALL)
        
        for language, filename, content in matches:
            files.append({
                "name": filename.strip(),
                "content": content.strip(),
                "language": language.strip()
            })
        
        # If no structured files found, create a basic structure
        if not files:
            # Create a simple project structure based on the prompt
            files = create_basic_project_structure(original_prompt, result_text)
        
        return ProjectResponse(
            files=files,
            output=result_text
        )
        
    except Exception as e:
        logger.error(f"Error parsing crew result: {e}")
        # Return basic response
        return ProjectResponse(
            files=[],
            output=str(result)
        )

def create_basic_project_structure(prompt: str, result_text: str) -> List[dict]:
    """Create basic project structure when parsing fails"""
    files = []
    
    # Determine project type from prompt
    prompt_lower = prompt.lower()
    
    if "react" in prompt_lower or "frontend" in prompt_lower:
        files.extend([
            {
                "name": "package.json",
                "content": json.dumps({
                    "name": "generated-app",
                    "version": "1.0.0",
                    "dependencies": {
                        "react": "^18.0.0",
                        "react-dom": "^18.0.0"
                    }
                }, indent=2),
                "language": "json"
            },
            {
                "name": "src/App.js",
                "content": "import React from 'react';\n\nexport default function App() {\n  return <div>Generated React App</div>;\n}",
                "language": "javascript"
            }
        ])
    elif "flutter" in prompt_lower or "mobile" in prompt_lower:
        files.extend([
            {
                "name": "pubspec.yaml",
                "content": "name: generated_app\nversion: 1.0.0\ndependencies:\n  flutter:\n    sdk: flutter",
                "language": "yaml"
            },
            {
                "name": "lib/main.dart",
                "content": "import 'package:flutter/material.dart';\n\nvoid main() {\n  runApp(MyApp());\n}\n\nclass MyApp extends StatelessWidget {\n  @override\n  Widget build(BuildContext context) {\n    return MaterialApp(home: Scaffold(body: Text('Generated Flutter App')));\n  }\n}",
                "language": "dart"
            }
        ])
    else:
        # Generic structure
        files.append({
            "name": "README.md",
            "content": f"# Generated Project\n\nGenerated from prompt: {prompt}\n\n## Result\n\n{result_text}",
            "language": "markdown"
        })
    
    return files

def save_project_manifest(project_id: str, prompt: Prompt, response: ProjectResponse):
    """Save project manifest to file"""
    try:
        manifest = {
            "project_id": project_id,
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt.dict(),
            "response": response.dict(),
            "files_count": len(response.files)
        }
        
        manifest_file = PROJECTS_DIR / f"{project_id}_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
            
        logger.info(f"Project manifest saved: {manifest_file}")
        
    except Exception as e:
        logger.error(f"Failed to save project manifest: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 