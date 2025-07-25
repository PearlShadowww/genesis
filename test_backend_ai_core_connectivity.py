#!/usr/bin/env python3
"""
Test Backend-AI Core Connectivity and Alignment
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BACKEND_URL = "http://localhost:8080"
AI_CORE_URL = "http://localhost:8000"
OLLAMA_URL = "http://localhost:11434"

def test_service_health(service_name: str, url: str, endpoint: str = "/health") -> bool:
    """Test if a service is healthy"""
    try:
        response = requests.get(f"{url}{endpoint}", timeout=10)
        if response.status_code == 200:
            print(f"✅ {service_name} is healthy")
            return True
        else:
            print(f"❌ {service_name} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name} is unreachable: {e}")
        return False

def test_ollama_models() -> bool:
    """Test if Ollama has required models"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            print(f"📦 Available Ollama models: {model_names}")
            
            required_models = ["qwen2.5-coder:1.5b-base", "llama3.1:8b"]
            missing_models = [m for m in required_models if m not in model_names]
            
            if missing_models:
                print(f"⚠️  Missing models: {missing_models}")
                return False
            else:
                print("✅ All required models are available")
                return True
        else:
            print(f"❌ Ollama API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False

def test_backend_ai_core_communication() -> bool:
    """Test direct communication between backend and AI core"""
    try:
        # Test backend health (which should check AI core)
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Backend health response: {json.dumps(data, indent=2)}")
            
            # Check if AI core is reported as healthy
            services = data.get("data", {}).get("services", {})
            ai_core_status = services.get("ai_core", "unknown")
            
            if ai_core_status == "healthy":
                print("✅ Backend reports AI core as healthy")
                return True
            else:
                print(f"⚠️  Backend reports AI core as: {ai_core_status}")
                return False
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend-AI core communication test failed: {e}")
        return False

def test_data_structure_alignment() -> bool:
    """Test if data structures are properly aligned"""
    try:
        # Test AI core health endpoint structure
        ai_response = requests.get(f"{AI_CORE_URL}/health", timeout=10)
        if ai_response.status_code == 200:
            ai_data = ai_response.json()
            print(f"📊 AI Core health structure: {json.dumps(ai_data, indent=2)}")
            
            # Check if response has expected structure
            if "success" in ai_data and "data" in ai_data:
                print("✅ AI Core response structure is correct")
                return True
            else:
                print("❌ AI Core response structure is incorrect")
                return False
        else:
            print(f"❌ AI Core health check failed: {ai_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Data structure test failed: {e}")
        return False

def test_project_generation_flow() -> bool:
    """Test the complete project generation flow"""
    try:
        # Test simple generation request
        test_prompt = "Create a simple React counter component"
        
        print(f"🧪 Testing project generation with prompt: {test_prompt}")
        
        # Send request to backend
        request_data = {
            "prompt": test_prompt,
            "backend": "ollama"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/generate",
            json=request_data,
            timeout=30
        )
        
        if response.status_code == 202:  # Accepted
            data = response.json()
            project_id = data.get("data")
            print(f"✅ Project generation started: {project_id}")
            
            # Wait a bit and check project status
            time.sleep(2)
            
            status_response = requests.get(f"{BACKEND_URL}/projects/{project_id}", timeout=10)
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"📊 Project status: {json.dumps(status_data, indent=2)}")
                return True
            else:
                print(f"❌ Failed to get project status: {status_response.status_code}")
                return False
        else:
            print(f"❌ Project generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Project generation flow test failed: {e}")
        return False

def main():
    """Run all connectivity tests"""
    print("🔍 Backend-AI Core Connectivity Test")
    print("=" * 50)
    
    # Test individual services
    services_healthy = True
    
    print("\n1. Testing individual services...")
    services_healthy &= test_service_health("Ollama", OLLAMA_URL, "/api/tags")
    services_healthy &= test_service_health("AI Core", AI_CORE_URL)
    services_healthy &= test_service_health("Backend", BACKEND_URL)
    
    print("\n2. Testing Ollama models...")
    models_available = test_ollama_models()
    
    print("\n3. Testing backend-AI core communication...")
    communication_ok = test_backend_ai_core_communication()
    
    print("\n4. Testing data structure alignment...")
    structure_ok = test_data_structure_alignment()
    
    print("\n5. Testing project generation flow...")
    generation_ok = test_project_generation_flow()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   Services Health: {'✅' if services_healthy else '❌'}")
    print(f"   Models Available: {'✅' if models_available else '❌'}")
    print(f"   Communication: {'✅' if communication_ok else '❌'}")
    print(f"   Data Alignment: {'✅' if structure_ok else '❌'}")
    print(f"   Generation Flow: {'✅' if generation_ok else '❌'}")
    
    overall_success = services_healthy and models_available and communication_ok and structure_ok and generation_ok
    
    if overall_success:
        print("\n🎉 All tests passed! Backend and AI core are properly aligned.")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
    
    return overall_success

if __name__ == "__main__":
    main() 