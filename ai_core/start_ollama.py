#!/usr/bin/env python3
"""
Ollama startup and validation script for Genesis
"""

import requests
import subprocess
import sys
import time
from pathlib import Path

def check_ollama_running():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Start Ollama if not running"""
    print("�� Starting Ollama...")
    
    try:
        # Try to start Ollama
        if sys.platform == "win32":
            subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["ollama", "serve"])
        
        # Wait for Ollama to start
        print("⏳ Waiting for Ollama to start...")
        for i in range(30):  # Wait up to 30 seconds
            if check_ollama_running():
                print("✅ Ollama started successfully")
                return True
            time.sleep(1)
            print(f"   {i+1}/30 seconds...")
        
        print("❌ Ollama failed to start within 30 seconds")
        return False
        
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama from https://ollama.ai/")
        return False
    except Exception as e:
        print(f"❌ Failed to start Ollama: {e}")
        return False

def check_required_models():
    """Check if required models are available"""
    print("📋 Checking required models...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            
            required_models = [
                "qwen2.5-coder:1.5b-base",
                "llama3.1:8b",
                "phi3:mini"
            ]
            
            available = []
            missing = []
            
            for required in required_models:
                if any(required in name for name in model_names):
                    available.append(required)
                    print(f"✅ {required}")
                else:
                    missing.append(required)
                    print(f"❌ {required}")
            
            return available, missing
        else:
            print("❌ Failed to get model list")
            return [], required_models
            
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return [], ["qwen2.5-coder:1.5b-base", "llama3.1:8b", "phi3:mini"]

def download_missing_models(missing_models):
    """Download missing models"""
    if not missing_models:
        return True
    
    print(f"\n�� Downloading {len(missing_models)} missing models...")
    
    for model in missing_models:
        print(f"�� Downloading {model}...")
        try:
            result = subprocess.run(
                ["ollama", "pull", model],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )
            
            if result.returncode == 0:
                print(f"✅ {model} downloaded successfully")
            else:
                print(f"❌ Failed to download {model}: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ Download timeout for {model}")
            return False
        except Exception as e:
            print(f"❌ Error downloading {model}: {e}")
            return False
    
    return True

def start_ai_core():
    """Start the AI core server"""
    print("\n🚀 Starting Genesis AI Core...")
    
    try:
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
        print(f"❌ Failed to start AI core: {e}")

def main():
    """Main startup function"""
    print("🎯 Genesis Ollama Startup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Please run this script from the ai_core directory")
        sys.exit(1)
    
    # Check if Ollama is running
    if not check_ollama_running():
        print("⚠️  Ollama is not running")
        if not start_ollama():
            sys.exit(1)
    else:
        print("✅ Ollama is already running")
    
    # Check required models
    available, missing = check_required_models()
    
    if missing:
        print(f"\n⚠️  {len(missing)} required models are missing")
        response = input("Download missing models? (y/N): ")
        
        if response.lower() == 'y':
            if not download_missing_models(missing):
                print("❌ Failed to download some models")
                print("You can download them manually:")
                for model in missing:
                    print(f"  ollama pull {model}")
                sys.exit(1)
        else:
            print("⚠️  Some models are missing. Performance may be limited.")
    
    # Start AI core
    start_ai_core()

if __name__ == "__main__":
    main() 