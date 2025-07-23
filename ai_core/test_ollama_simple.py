#!/usr/bin/env python3
"""
Simple test script to check Ollama connection and available models
"""

import requests
import json

def test_ollama():
    print("🔍 Testing Ollama connection...")
    
    try:
        # Test if Ollama is running
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            
            print(f"✅ Ollama is running with {len(models)} models:")
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
        print(f"❌ Error: {e}")
        return False, []

def test_model_generation(model_name):
    print(f"\n🤖 Testing model: {model_name}")
    
    try:
        payload = {
            "model": model_name,
            "prompt": "Say hello",
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generation successful: {data.get('response', '')[:50]}...")
            return True
        else:
            print(f"❌ Generation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Simple Ollama Test")
    print("=" * 30)
    
    success, models = test_ollama()
    
    if success and models:
        # Test first model
        model_name = models[0].get('name', '')
        if model_name:
            test_model_generation(model_name)
    else:
        print("\n❌ Cannot test generation without available models") 