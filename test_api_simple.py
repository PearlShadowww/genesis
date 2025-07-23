#!/usr/bin/env python3
"""
Simple API test for Genesis
"""

import requests


def test_api():
    """Test the Genesis API endpoints"""
    
    print("🧪 Testing Genesis API...")
    
    # Test health endpoint
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test project generation
    try:
        payload = {
            "prompt": "Create a simple React counter component",
            "backend": "ollama"
        }
        
        print("\n🚀 Testing project generation...")
        response = requests.post(
            "http://127.0.0.1:8000/run",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Project generation successful!")
            print(f"📁 Generated {len(data.get('files', []))} files")
            print(f"📝 Output length: {len(data.get('output', ''))} characters")
        else:
            print(f"❌ Project generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Project generation error: {e}")


if __name__ == "__main__":
    test_api() 