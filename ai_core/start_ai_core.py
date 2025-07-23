#!/usr/bin/env python3
"""
Startup script for Genesis AI Core
"""

import subprocess
import requests
import time
import sys
import os
from pathlib import Path

def check_ollama():
    """Check if Ollama is running and has required models"""
    try:
        # Check if Ollama is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            
            # Check for required models
            required_models = ["qwen2.5-coder:1.5b-base", "llama3.1:8b"]
            available_models = []
            
            for required in required_models:
                if any(required in name for name in model_names):
                    available_models.append(required)
            
            if available_models:
                print(f"✅ Ollama is running with models: {', '.join(available_models)}")
                return True
            else:
                print("⚠️  Ollama is running but no required models found")
                print("Run: ollama pull qwen2.5-coder:1.5b-base")
                return False
        else:
            print("❌ Ollama is not responding")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Ollama is not running")
        print("Start Ollama with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    try:
        print("🚀 Starting Genesis AI Core server...")
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main startup function"""
    print("🎯 Genesis AI Core Startup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Please run this script from the ai_core directory")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check Ollama
    if not check_ollama():
        print("\n💡 To fix Ollama issues:")
        print("1. Install Ollama from https://ollama.ai/")
        print("2. Run: ollama serve")
        print("3. Run: ollama pull qwen2.5-coder:1.5b-base")
        print("\nContinue anyway? (y/N): ", end="")
        
        if input().lower() != 'y':
            sys.exit(1)
    
    print("\n�� All checks passed! Starting server...")
    start_server()

if __name__ == "__main__":
    main() 