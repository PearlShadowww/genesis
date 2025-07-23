#!/usr/bin/env python3
"""
Enhanced logging configuration for Genesis AI Core
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "detailed"
) -> logging.Logger:
    """
    Setup comprehensive logging for Genesis AI Core
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        log_format: Log format style (simple, detailed, json)
    
    Returns:
        Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Choose format based on style
    if log_format == "simple":
        console_format = "%(levelname)s: %(message)s"
        file_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    elif log_format == "json":
        console_format = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        file_format = console_format
    else:  # detailed
        console_format = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
        file_format = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)s:%(lineno)d | %(message)s"
    
    # Apply colored formatter to console
    console_formatter = ColoredFormatter(console_format, datefmt="%H:%M:%S")
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        # Rotating file handler (10MB per file, keep 5 files)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        file_formatter = logging.Formatter(file_format, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Create specific logger for Genesis
    logger = logging.getLogger("genesis")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Add specific handlers for different components
    setup_component_loggers()
    
    return logger

def setup_component_loggers():
    """Setup specific loggers for different components"""
    
    # CrewAI logger
    crewai_logger = logging.getLogger("crewai")
    crewai_logger.setLevel(logging.INFO)
    
    # Ollama logger
    ollama_logger = logging.getLogger("ollama")
    ollama_logger.setLevel(logging.INFO)
    
    # FastAPI logger
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(logging.INFO)
    
    # Uvicorn logger
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)

def get_logger(name: str = "genesis") -> logging.Logger:
    """Get a logger instance with the given name"""
    return logging.getLogger(name)

class RequestLogger:
    """Middleware for logging HTTP requests"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    async def log_request(self, request, response, duration: float):
        """Log request details"""
        self.logger.info(
            f"Request: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.3f}s"
        )

def log_function_call(func_name: str, args: dict = None, result: any = None):
    """Decorator for logging function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger("genesis.functions")
            logger.debug(f"Calling {func_name} with args: {args}, kwargs: {kwargs}")
            
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func_name} returned: {result}")
                return result
            except Exception as e:
                logger.error(f"{func_name} failed with error: {e}")
                raise
        
        return wrapper
    return decorator

# Environment-based configuration
def get_logging_config():
    """Get logging configuration from environment variables"""
    return {
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "log_file": os.getenv("LOG_FILE", "logs/genesis.log"),
        "log_format": os.getenv("LOG_FORMAT", "detailed")
    }

# Initialize logging on import
if __name__ != "__main__":
    config = get_logging_config()
    setup_logging(**config) 