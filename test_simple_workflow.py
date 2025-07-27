#!/usr/bin/env python3
"""
Simple test script to verify the complete Genesis workflow
Tests: Frontend -> Backend -> AI Core -> Ollama -> File Generation
"""

import requests
import time
import sys
from datetime import datetime


def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get('http://127.0.0.1:8080/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is healthy")
            status = data.get('data', {}).get('status', 'unknown')
            print(f"   Status: {status}")
            services = data.get('data', {}).get('services', {})
            print(f"   Services: {services}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend is not reachable: {e}")
        return False


def test_ai_core_health():
    """Test if AI core is running"""
    try:
        response = requests.get('http://127.0.0.1:8000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ AI Core is healthy")
            status = data.get('data', {}).get('status', 'unknown')
            print(f"   Status: {status}")
            return True
        else:
            print(f"❌ AI Core health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI Core is not reachable: {e}")
        return False


def test_ollama_connection():
    """Test if Ollama is running"""
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama3.1:8b",
                "prompt": "Hello, this is a test.",
                "stream": False
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Ollama is running and responding")
            return True
        else:
            print(f"❌ Ollama test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama is not reachable: {e}")
        return False

def test_project_generation():
    """Test complete project generation workflow"""
    print("\n🚀 Testing project generation...")
    
    test_prompt = "Create a simple React todo app with add and delete functionality"
    
    try:
        # Start generation
        response = requests.post(
            'http://127.0.0.1:8080/generate',
            json={
                "prompt": test_prompt,
                "backend": "ollama"
            },
            timeout=10
        )
        
        if response.status_code != 202:
            print(f"❌ Generation request failed: {response.status_code}")
            return False
            
        result = response.json()
        project_id = result.get('data')
        print(f"✅ Generation started with project ID: {project_id}")
        
        # Poll for completion
        max_attempts = 30
        attempts = 0
        
        while attempts < max_attempts:
            try:
                status_response = requests.get(f'http://127.0.0.1:8080/projects/{project_id}', timeout=5)
                
                if status_response.status_code == 200:
                    project_data = status_response.json().get('data', {})
                    status = project_data.get('status')
                    
                    print(f"   Status: {status}")
                    
                    if status == 'completed':
                        files = project_data.get('files', [])
                        print(f"✅ Project completed successfully!")
                        print(f"   Generated {len(files)} files:")
                        for file in files:
                            print(f"   - {file.get('name')} ({file.get('language')})")
                        return True
                        
                    elif status == 'failed':
                        error_msg = project_data.get('output', 'Unknown error')
                        print(f"❌ Project generation failed: {error_msg}")
                        return False
                        
                    else:
                        # Still generating, wait and try again
                        time.sleep(1)
                        attempts += 1
                        
                else:
                    print(f"❌ Failed to get project status: {status_response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ Error polling project status: {e}")
                attempts += 1
                time.sleep(1)
        
        print("⏰ Project generation timed out")
        return False
        
    except Exception as e:
        print(f"❌ Project generation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Genesis Workflow Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test all components
    tests = [
        ("Backend Health", test_backend_health),
        ("AI Core Health", test_ai_core_health),
        ("Ollama Connection", test_ollama_connection),
        ("Project Generation", test_project_generation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Genesis workflow is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the services and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 