from pydantic import BaseModel
from typing import List, Optional

class Prompt(BaseModel):
    prompt: str
    backend: str = "ollama"

class GeneratedFile(BaseModel):
    name: str
    content: str
    language: str

class ProjectResponse(BaseModel):
    files: List[GeneratedFile]
    output: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: dict 