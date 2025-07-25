from langchain_ollama import OllamaLLM
import logging
from typing import List, Any, Dict
from langchain.schema import BaseMessage

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

class CrewAIOllamaAdapter:
    """Adapter to make LangChain Ollama work with CrewAI"""
    
    def __init__(self, model_name: str, base_url: str = "http://localhost:11434", temperature: float = 0.1):
        self.ollama_llm = OllamaLLM(
            model=model_name,
            base_url=base_url,
            temperature=temperature,
            verbose=False
        )
        self.model_name = model_name
    
    def call(self, messages: List[BaseMessage], **kwargs) -> str:
        """Convert CrewAI call to LangChain invoke"""
        try:
            # Convert messages to a single prompt
            prompt = self._messages_to_prompt(messages)
            response = self.ollama_llm.invoke(prompt)
            return str(response)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise e
    
    def _messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        """Convert message list to a single prompt string"""
        prompt_parts = []
        for message in messages:
            if hasattr(message, 'content'):
                prompt_parts.append(str(message.content))
            else:
                prompt_parts.append(str(message))
        
        return "\n\n".join(prompt_parts)

def get_llm():
    """Get configured Ollama LLM instance"""
    try:
        # Check available models
        available_models = get_available_models()
        logger.info(f"Available models: {available_models}")
        
        # Use a simple model name that should work
        model_name = "llama3.1:8b"  # Use a known working model
        
        if model_name not in available_models:
            # Fallback to first available model
            if available_models:
                model_name = available_models[0]
                logger.warning(f"Preferred model not found, using: {model_name}")
            else:
                raise Exception("No Ollama models available. Please install a model first.")
        
        logger.info(f"Using model: {model_name}")
        
        # Use direct LangChain Ollama with exact model name
        llm = OllamaLLM(
            model=model_name,  # Use the exact model name from Ollama
            base_url="http://localhost:11434",
            temperature=0.1,
            verbose=False
        )
        
        logger.info(f"LLM connection successful (LangChain direct) - using model: {model_name}")
        return llm
        
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise Exception(f"LLM initialization failed: {str(e)}") 