#!/usr/bin/env python3
"""
Comprehensive Ollama test script for Genesis
"""

import sys
from typing import List, Tuple, Dict, Any

import requests


def test_ollama_connection() -> Tuple[bool, List[Dict[str, Any]]]:
    """Test basic Ollama connectivity"""
    print("🔍 Testing Ollama connection...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"✅ Ollama is running with {len(models)} models")
            
            for model in models:
                name = model.get('name', 'Unknown')
                size_mb = model.get('size', 0) / (1024 * 1024)
                print(f"  - {name} ({size_mb:.1f} MB)")
            
            return True, models
        else:
            print(f"❌ Ollama returned status {response.status_code}")
            return False, []
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to Ollama")
        print("💡 Make sure Ollama is running: ollama serve")
        return False, []
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False, []


def test_model_generation(model_name: str) -> bool:
    """Test model generation capabilities"""
    print(f"\n🤖 Testing model: {model_name}")
    
    try:
        # Test simple generation
        payload = {
            "model": model_name,
            "prompt": "Write a simple JS function that adds two numbers",
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            generated_text = data.get('response', '')
            print(f"✅ Generation successful ({len(generated_text)} chars)")
            print(f"Sample: {generated_text[:100]}...")
            return True
        else:
            print(f"❌ Generation failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False


def test_required_models() -> List[str]:
    """Test if required models are available"""
    print("\n📋 Checking required models...")
    
    required_models = [
        "qwen2.5-coder:1.5b-base",
        "llama3.1:8b",
        "phi3:mini"
    ]
    
    available_models: List[str] = []
    _, models = test_ollama_connection()
    
    if models:
        available_names = [model.get('name', '') for model in models]
        
        for required in required_models:
            if any(required in name for name in available_names):
                available_models.append(required)
                print(f"✅ {required} - Available")
            else:
                print(f"❌ {required} - Missing")
    
    return available_models


def test_crewai_integration() -> bool:
    """Test CrewAI integration with Ollama"""
    print("\n👥 Testing CrewAI integration...")
    
    try:
        from llm import get_llm
        from agents import create_agents
        from tasks import create_tasks
        
        # Test LLM initialization
        llm = get_llm()
        print("✅ LLM initialized successfully")
        
        # Test agent creation
        agents = create_agents(llm)
        print(f"✅ Created {len(agents)} agents")
        
        # Test task creation
        tasks = create_tasks("Create a simple React counter app")
        print(f"✅ Created {len(tasks)} tasks")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ CrewAI integration error: {e}")
        return False


def test_api_endpoints() -> None:
    """Test API endpoints if server is running"""
    print("\n🌐 Testing API endpoints...")
    
    endpoints = [
        ("Health", "http://127.0.0.1:8000/health"),
        ("Root", "http://127.0.0.1:8000/"),
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} endpoint - Working")
            else:
                print(f"❌ {name} endpoint - Status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"⚠️  {name} endpoint - Server not running")
        except Exception as e:
            print(f"❌ {name} endpoint - Error: {e}")


def provide_setup_instructions() -> None:
    """Provide setup instructions if tests fail"""
    print("\n Setup Instructions:")
    print("=" * 40)
    print("1. Install Ollama from https://ollama.ai/")
    print("2. Start Ollama: ollama serve")
    print("3. Download required models:")
    print("   ollama pull qwen2.5-coder:1.5b-base")
    print("   ollama pull llama3.1:8b")
    print("   ollama pull phi3:mini")
    print("4. Install Python dependencies:")
    print("   cd ai_core && pip install -r requirements.txt")
    print("5. Run this test again")


def main() -> None:
    """Run comprehensive Ollama tests"""
    print("🧪 Genesis Ollama Test Suite")
    print("=" * 40)
    
    # Test connection
    connection_ok, _ = test_ollama_connection()
    
    if not connection_ok:
        provide_setup_instructions()
        sys.exit(1)
    
    # Test required models
    available_models = test_required_models()
    
    if not available_models:
        print("\n⚠️  No required models found")
        provide_setup_instructions()
        sys.exit(1)
    
    # Test model generation
    generation_tests = []
    for model in available_models[:2]:  # Test first 2 models
        success = test_model_generation(model)
        generation_tests.append(success)
    
    # Test CrewAI integration
    crewai_ok = test_crewai_integration()
    
    # Test API endpoints
    test_api_endpoints()
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 40)
    print(f"Connection: {'✅' if connection_ok else '❌'}")
    print(f"Models Available: {len(available_models)}/{3}")
    passed_tests = sum(generation_tests)
    total_tests = len(generation_tests)
    print(f"Generation Tests: {passed_tests}/{total_tests} passed")
    print(f"CrewAI Integration: {'✅' if crewai_ok else '❌'}")
    
    if connection_ok and available_models and crewai_ok:
        print("\n🎉 Ollama is ready for Genesis!")
        print("You can now start the AI core server.")
    else:
        print("\n⚠️  Some tests failed. Check the setup instructions above.")


if __name__ == "__main__":
    main() 