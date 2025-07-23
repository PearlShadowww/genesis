#!/usr/bin/env python3
"""
Enhanced error handling for Genesis AI Core
"""

import asyncio
import functools
import logging
import traceback
from typing import Any, Callable, Dict, Optional, Type, Union
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import ValidationError

logger = logging.getLogger("genesis.errors")

class GenesisError(Exception):
    """Base exception for Genesis AI Core"""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "GENESIS_ERROR"
        self.details = details or {}
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }

class OllamaError(GenesisError):
    """Exception for Ollama-related errors"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "OLLAMA_ERROR", details)

class CrewAIError(GenesisError):
    """Exception for CrewAI-related errors"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "CREWAI_ERROR", details)

class ValidationError(GenesisError):
    """Exception for validation errors"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "VALIDATION_ERROR", details)

class TimeoutError(GenesisError):
    """Exception for timeout errors"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "TIMEOUT_ERROR", details)

class ResourceError(GenesisError):
    """Exception for resource-related errors"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "RESOURCE_ERROR", details)

def handle_exceptions(func: Callable) -> Callable:
    """Decorator to handle exceptions and convert them to appropriate HTTP responses"""
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        
        except GenesisError as e:
            logger.error(f"Genesis error in {func.__name__}: {e.message}", extra=e.details)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.to_dict()
            )
        
        except ValidationError as e:
            logger.error(f"Validation error in {func.__name__}: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": "VALIDATION_ERROR",
                    "message": "Invalid request data",
                    "details": str(e)
                }
            )
        
        except TimeoutError as e:
            logger.error(f"Timeout error in {func.__name__}: {e}")
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail={
                    "error": "TIMEOUT_ERROR",
                    "message": "Request timed out",
                    "details": str(e)
                }
            )
        
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                    "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None
                }
            )
    
    return wrapper

def retry_on_failure(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """Decorator to retry operations on failure"""
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    if asyncio.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"Max retries ({max_retries}) exceeded for {func.__name__}: {e}")
                        raise
                    
                    wait_time = delay * (backoff_factor ** attempt)
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {wait_time:.2f}s..."
                    )
                    
                    await asyncio.sleep(wait_time)
            
            # This should never be reached, but just in case
            raise last_exception
        
        return wrapper
    return decorator

def validate_ollama_response(response: Dict[str, Any]) -> None:
    """Validate Ollama API response"""
    if not isinstance(response, dict):
        raise OllamaError("Invalid response format from Ollama")
    
    if "error" in response:
        raise OllamaError(f"Ollama error: {response['error']}")
    
    if "response" not in response:
        raise OllamaError("Missing 'response' field in Ollama response")

def validate_crewai_result(result: Any) -> None:
    """Validate CrewAI result"""
    if result is None:
        raise CrewAIError("CrewAI returned None result")
    
    if isinstance(result, str) and not result.strip():
        raise CrewAIError("CrewAI returned empty result")

def safe_json_parse(data: str, context: str = "JSON parsing") -> Dict[str, Any]:
    """Safely parse JSON with error handling"""
    try:
        import json
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ValidationError(f"{context} failed: {e}")

def log_function_call(func_name: str) -> Callable:
    """Decorator to log function calls with timing"""
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            logger.debug(f"Calling {func_name} with args: {args}, kwargs: {kwargs}")
            
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.debug(f"{func_name} completed in {duration:.3f}s")
                return result
            
            except Exception as e:
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.error(f"{func_name} failed after {duration:.3f}s: {e}")
                raise
        
        return wrapper
    return decorator

# Global error handlers
def setup_error_handlers(app):
    """Setup global error handlers for FastAPI app"""
    
    @app.exception_handler(GenesisError)
    async def genesis_error_handler(request, exc: GenesisError):
        logger.error(f"Genesis error: {exc.message}", extra=exc.details)
        return {
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details,
            "timestamp": exc.timestamp.isoformat()
        }
    
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request, exc: ValidationError):
        logger.error(f"Validation error: {exc}")
        return {
            "error": "VALIDATION_ERROR",
            "message": "Invalid request data",
            "details": str(exc)
        }
    
    @app.exception_handler(Exception)
    async def general_error_handler(request, exc: Exception):
        logger.error(f"Unexpected error: {exc}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
            "details": str(exc) if logger.isEnabledFor(logging.DEBUG) else None
        } 