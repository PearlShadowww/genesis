from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


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


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, Any]


# Backend-compatible structures
class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class ProjectStatus(str, Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectRecord(BaseModel):
    id: str
    prompt: str
    files: List[GeneratedFile]
    output: str
    created_at: datetime
    status: ProjectStatus 