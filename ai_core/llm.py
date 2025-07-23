from langchain_ollama import OllamaLLM
import logging
from typing import List

import requests

logger = logging.getLogger(__name__)


def get_available_models() -> List[str]:
    """Get list of available Ollama models"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        return []
    except Exception as e:
        logger.error(f"Failed to get available models: {e}")
        return []

def get_llm():
    """Get configured Ollama LLM instance"""
    try:
        # Check available models
        available_models = get_available_models()
        logger.info(f"Available models: {available_models}")
        
        # Try to use a common model, fallback to first available
        preferred_models = [
            "qwen2.5-coder:1.5b-base",  # Smaller model, might be more compatible
            "llama3.1:8b",
            "phi3:mini",
            "llama3.1:3b"
        ]
        
        model_name = None
        for model in preferred_models:
            if model in available_models:
                model_name = model
                break
        
        if not model_name and available_models:
            model_name = available_models[0]
            logger.warning(f"No preferred model found, using: {model_name}")
        
        if not model_name:
            raise Exception("No Ollama models available. Please install a model first.")
        
        logger.info(f"Using model: {model_name}")
        
        # Use LangChain Ollama with minimal configuration
        llm = OllamaLLM(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0.1,  # Lower temperature for more consistent output
            verbose=False  # Disable verbose to reduce noise
        )
        
        logger.info("LLM connection successful")
        
        return llm
        
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise Exception(f"LLM initialization failed: {str(e)}") 