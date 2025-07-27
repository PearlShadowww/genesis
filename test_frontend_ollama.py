#!/usr/bin/env python3
"""
Test script to verify frontend -> Ollama communication
Sends "hi" from frontend and captures the LLM reply
"""

import requests
import time
import json
from datetime import datetime

def test_direct_ollama():
    """Test direct communication with Ollama"""
    print("🔍 Testing direct Ollama communication...")
    
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama3.1:8b",
                "prompt": "hi",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get('response', '')
            print(f"✅ Direct Ollama test successful")
            print(f"   Prompt: hi")
            print(f"   Reply: {reply[:200]}...")
            return True
        else:
            print(f"❌ Direct Ollama test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Direct Ollama test error: {e}")
        return False

def test_frontend_workflow():
    """Test complete frontend -> backend -> ai_core -> ollama workflow"""
    print("\n🚀 Testing frontend workflow with 'hi' prompt...")
    
    try:
        # Step 1: Send generation request to backend
        print("   📤 Sending request to backend...")
        response = requests.post(
            'http://127.0.0.1:8080/generate',
            json={
                "prompt": "hi",
                "backend": "ollama"
            },
            timeout=10
        )
        
        if response.status_code != 202:
            print(f"   ❌ Backend request failed: {response.status_code}")
            return False
            
        result = response.json()
        project_id = result.get('data')
        print(f"   ✅ Backend accepted request, project ID: {project_id}")
        
        # Step 2: Poll for completion
        print("   🔄 Polling for completion...")
        max_attempts = 30
        attempts = 0
        
        while attempts < max_attempts:
            try:
                status_response = requests.get(
                    f'http://127.0.0.1:8080/projects/{project_id}', 
                    timeout=5
                )
                
                if status_response.status_code == 200:
                    project_data = status_response.json().get('data', {})
                    status = project_data.get('status')
                    
                    print(f"   📊 Status: {status}")
                    
                    if status == 'completed':
                        files = project_data.get('files', [])
                        output = project_data.get('output', '')
                        
                        print(f"   ✅ Project completed!")
                        print(f"   📁 Generated {len(files)} files:")
                        for file in files:
                            print(f"      - {file.get('name')} ({file.get('language')})")
                            content = file.get('content', '')[:100]
                            print(f"        Content preview: {content}...")
                        
                        print(f"   📝 AI Core output: {output[:200]}...")
                        return True
                        
                    elif status == 'failed':
                        error_msg = project_data.get('output', 'Unknown error')
                        print(f"   ❌ Project failed: {error_msg}")
                        return False
                        
                    else:
                        # Still generating, wait and try again
                        time.sleep(1)
                        attempts += 1
                        
                else:
                    print(f"   ❌ Status check failed: {status_response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Status polling error: {e}")
                attempts += 1
                time.sleep(1)
        
        print("   ⏰ Project generation timed out")
        return False
        
    except Exception as e:
        print(f"   ❌ Frontend workflow test failed: {e}")
        return False

def test_ai_core_direct():
    """Test direct communication with AI Core"""
    print("\n🔍 Testing direct AI Core communication...")
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/run',
            json={
                "prompt": "hi",
                "backend": "ollama"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            files = data.get('data', {}).get('files', [])
            output = data.get('data', {}).get('output', '')
            
            print(f"✅ Direct AI Core test successful")
            print(f"   Prompt: hi")
            print(f"   Generated {len(files)} files:")
            for file in files:
                print(f"      - {file.get('name')} ({file.get('language')})")
                content = file.get('content', '')[:100]
                print(f"        Content: {content}...")
            print(f"   Output: {output[:200]}...")
            return True
        else:
            print(f"❌ Direct AI Core test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Direct AI Core test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Frontend -> Ollama Communication Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test all communication paths
    tests = [
        ("Direct Ollama", test_direct_ollama),
        ("Direct AI Core", test_ai_core_direct),
        ("Frontend Workflow", test_frontend_workflow),
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
        print("🎉 All tests passed! Frontend -> Ollama communication is working.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the services and try again.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main()) 