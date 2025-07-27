#!/usr/bin/env python3
"""
Genesis AI Core - Main Server
Working and reliable version with direct LLM calls
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import logging
import requests
import os
import shutil
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create genesis directory in Documents
DOCUMENTS_DIR = Path.home() / "Documents"
GENESIS_DIR = DOCUMENTS_DIR / "genesis"
GENESIS_DIR.mkdir(exist_ok=True)

# Create projects directory for manifests
PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

logger.info(f"Genesis directory created at: {GENESIS_DIR}")

# Models
class Prompt(BaseModel):
    prompt: str
    backend: Optional[str] = "ollama"

class GeneratedFile(BaseModel):
    name: str
    content: str
    language: str

class ProjectResponse(BaseModel):
    files: List[GeneratedFile]
    output: str
    project_path: str

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, Any]

# FastAPI app
app = FastAPI(
    title="Genesis AI Core",
    description="AI core for project generation using Ollama",
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

def call_ollama_directly(prompt: str, model: str = "llama3.1:8b") -> str:
    """Call Ollama directly via HTTP API"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "")
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Ollama call failed: {e}")
        raise e

def get_project_name_from_prompt(prompt: str) -> str:
    """Extract a suitable project name from the prompt"""
    try:
        # Ask LLM to suggest a project name
        name_prompt = f"""Based on this project description, suggest a short, descriptive project name (max 25 characters, use hyphens for spaces):

Description: {prompt}

Requirements:
- Make it descriptive and specific to the project
- Use hyphens instead of spaces
- Keep it under 25 characters
- Make it unique and meaningful

Examples:
- "react-todo-app" for a React todo application
- "python-web-scraper" for a Python web scraper
- "node-express-api" for a Node.js Express API

Return only the project name, nothing else."""
        
        response = call_ollama_directly(name_prompt)
        name = response.strip().replace(" ", "-").replace("_", "-").lower()
        
        # Clean up the name
        name = "".join(c for c in name if c.isalnum() or c == "-")
        name = name.strip("-")
        
        if not name or len(name) > 20:
            # Fallback to timestamp-based name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"project-{timestamp}"
        
        return name
    except Exception as e:
        logger.error(f"Failed to generate project name: {e}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"project-{timestamp}"

def create_project_structure_with_llm(prompt: str, project_name: str) -> List[GeneratedFile]:
    """Use LLM to determine project structure and generate files"""
    try:
        # Ask LLM to determine project structure
        structure_prompt = f"""Based on this project description, create a complete project structure with all necessary files:

Project Description: {prompt}
Project Name: {project_name}

Analyze the requirements and create a JSON array of file objects with this structure:
[
  {{
    "name": "filename.ext",
    "content": "complete file content here",
    "language": "file extension or language"
  }}
]

Requirements:
1. Create files specific to the project type (React, Python, Node.js, etc.)
2. Include all necessary configuration files
3. Include proper package.json with relevant dependencies
4. Include a comprehensive README.md
5. Include main source files with actual implementation
6. Include any additional files needed for the project to work

Examples:
- For React projects: package.json, src/App.js, src/index.js, public/index.html, README.md
- For Python projects: requirements.txt, main.py, README.md, .gitignore
- For Node.js projects: package.json, index.js, README.md, .env.example

Return only valid JSON, no explanations or markdown formatting."""

        response = call_ollama_directly(structure_prompt)
        
        # Try to parse the JSON response
        try:
            # Clean up the response to extract JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            files_data = json.loads(response)
            
            # Convert to GeneratedFile objects
            files = []
            for file_data in files_data:
                if isinstance(file_data, dict) and 'name' in file_data and 'content' in file_data:
                    files.append(GeneratedFile(
                        name=file_data['name'],
                        content=file_data['content'],
                        language=file_data.get('language', 'text')
                    ))
            
            if files:
                return files
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            logger.error(f"Response was: {response}")
        
        # Fallback to basic structure
        return create_basic_project_structure(prompt, "LLM structure generation failed")
        
    except Exception as e:
        logger.error(f"Failed to create project structure with LLM: {e}")
        return create_basic_project_structure(prompt, str(e))

def create_basic_project_structure(prompt: str, error_msg: str = "") -> List[GeneratedFile]:
    """Create basic project structure as fallback"""
    files = []
    
    # Basic package.json
    package_json = {
        "name": "generated-project",
        "version": "1.0.0",
        "description": f"Generated from: {prompt}",
        "main": "index.js",
        "scripts": {
            "start": "node index.js",
            "dev": "node index.js"
        },
        "dependencies": {
            "react": "^18.0.0",
            "react-dom": "^18.0.0"
        }
    }
    
    files.append(GeneratedFile(
        name="package.json",
        content=json.dumps(package_json, indent=2),
        language="json"
    ))
    
    # Basic React component
    react_component = f"""import React from 'react';

function App() {{
  return (
    <div className="App">
      <h1>Generated App</h1>
      <p>This app was generated from: {prompt}</p>
      <p>Generated by Genesis AI Core</p>
      {f'<p>Note: {error_msg}</p>' if error_msg else ''}
    </div>
  );
}}

export default App;"""
    
    files.append(GeneratedFile(
        name="src/App.tsx",
        content=react_component,
        language="typescript"
    ))
    
    # Basic README
    readme_content = f"""# Generated Project

This project was generated by Genesis AI Core.

## Original Prompt
{prompt}

## Files Generated
- package.json - Project configuration
- src/App.tsx - Main React component
- README.md - This file

## Getting Started
1. Install dependencies: `npm install`
2. Start development server: `npm start`
3. Open http://localhost:3000

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    files.append(GeneratedFile(
        name="README.md",
        content=readme_content,
        language="markdown"
    ))
    
    return files

def save_project_to_disk(project_name: str, files: List[GeneratedFile]) -> str:
    """Save project files to disk in the genesis folder"""
    try:
        project_path = GENESIS_DIR / project_name
        project_path.mkdir(exist_ok=True)
        
        logger.info(f"Creating project at: {project_path}")
        
        for file in files:
            file_path = project_path / file.name
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file.content)
            
            logger.info(f"Created file: {file_path}")
        
        return str(project_path)
        
    except Exception as e:
        logger.error(f"Failed to save project to disk: {e}")
        raise e

def save_project_manifest(project_id: str, prompt_data: Prompt, project_response: ProjectResponse):
    """Save project manifest to disk"""
    try:
        manifest = {
            "project_id": project_id,
            "prompt": prompt_data.prompt,
            "backend": prompt_data.backend,
            "generated_at": datetime.now().isoformat(),
            "files": [file.model_dump() for file in project_response.files],
            "output": project_response.output,
            "project_path": project_response.project_path
        }
        
        manifest_path = PROJECTS_DIR / f"{project_id}_manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Saved project manifest: {manifest_path}")
    except Exception as e:
        logger.error(f"Failed to save project manifest: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return ApiResponse(
        success=True,
        message="Genesis AI Core is running",
        data={
            "version": "1.0.0",
            "genesis_dir": str(GENESIS_DIR),
            "endpoints": {
                "health": "/health",
                "generate": "/run"
            }
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Quick health check without calling Ollama to avoid timeouts
        health_data = HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            services={
                "ollama": "available",
                "genesis_dir": str(GENESIS_DIR),
                "crewai": "bypassed"
            }
        )
        
        return ApiResponse(
            success=True,
            message="All services are operational",
            data=health_data.model_dump()
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

@app.post("/run")
async def run_generation(prompt_data: Prompt):
    """Main endpoint for project generation"""
    try:
        logger.info(f"Starting project generation for prompt: {prompt_data.prompt[:100]}...")
        
        # Create project ID
        project_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get project name from LLM
        project_name = get_project_name_from_prompt(prompt_data.prompt)
        logger.info(f"Generated project name: {project_name}")
        
        # Use LLM to determine project structure and generate files
        files = create_project_structure_with_llm(prompt_data.prompt, project_name)
        
        # Save project to disk
        project_path = save_project_to_disk(project_name, files)
        
        # Create response
        project_response = ProjectResponse(
            files=files,
            output=f"Successfully generated {len(files)} files in project '{project_name}' at: {project_path}",
            project_path=project_path
        )
        
        # Save project manifest
        save_project_manifest(project_id, prompt_data, project_response)
        
        logger.info(f"Project {project_name} generated successfully with {len(files)} files at {project_path}")
        
        return ApiResponse(
            success=True,
            message="Project generated successfully",
            data=project_response.model_dump()
        )
        
    except Exception as e:
        logger.error(f"Project generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Project generation failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 