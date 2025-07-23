#!/usr/bin/env python3
"""
Comprehensive API testing script for Genesis
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List


def test_health_endpoint() -> bool:
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    
    try:
        response = requests.get(
            "http://127.0.0.1:8000/health",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Services: {data.get('services', {})}")
            return True
        else:
            print(f"❌ Health endpoint returned {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to AI core server")
        print("💡 Start the server: python start_ai_core.py")
        return False
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        return False


def test_root_endpoint() -> bool:
    """Test the root endpoint"""
    print("\n🏠 Testing root endpoint...")
    
    try:
        response = requests.get(
            "http://127.0.0.1:8000/",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint working")
            print(f"   Message: {data.get('message', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ Root endpoint returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Root test failed: {e}")
        return False


def test_project_generation() -> bool:
    """Test project generation endpoint"""
    print("\n🚀 Testing project generation...")
    
    test_prompt = "Create a simple React counter app with increment and decrement buttons"
    
    try:
        payload = {
            "prompt": test_prompt,
            "backend": "ollama"
        }
        
        print(f"   Prompt: {test_prompt[:50]}...")
        
        response = requests.post(
            "http://127.0.0.1:8000/run",
            json=payload,
            timeout=300  # 5 minutes timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            files = data.get('files', [])
            output = data.get('output', '')
            
            print("✅ Project generation successful")
            print(f"   Files generated: {len(files)}")
            print(f"   Output length: {len(output)} characters")
            
            # Show file names
            for file in files[:3]:  # Show first 3 files
                print(f"   - {file.get('name', 'unknown')}")
            
            if len(files) > 3:
                print(f"   ... and {len(files) - 3} more files")
            
            return True
        else:
            print(f"❌ Project generation failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Project generation timed out (5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Project generation test failed: {e}")
        return False


def test_backend_health() -> bool:
    """Test Rust backend health"""
    print("\n🔧 Testing Rust backend...")
    
    try:
        response = requests.get(
            "http://127.0.0.1:8080/health",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rust backend working")
            print(f"   Status: {data.get('data', {}).get('status', 'unknown')}")
            
            services = data.get('data', {}).get('services', {})
            for service, status in services.items():
                print(f"   {service}: {status}")
            
            return True
        else:
            print(f"❌ Rust backend returned {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Rust backend")
        print("💡 Start the backend: cd backend && cargo run")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False


def test_backend_generation() -> bool:
    """Test Rust backend project generation"""
    print("\n🔄 Testing backend project generation...")
    
    test_prompt = "Create a simple HTML page with a button"
    
    try:
        payload = {
            "prompt": test_prompt,
            "backend": "ollama"
        }
        
        print(f"   Prompt: {test_prompt}")
        
        response = requests.post(
            "http://127.0.0.1:8080/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 202:  # Accepted
            data = response.json()
            project_id = data.get('data')
            print(f"✅ Project generation started: {project_id}")
            
            # Wait for completion
            print("   Waiting for completion...")
            for i in range(60):  # Wait up to 60 seconds
                time.sleep(2)
                
                try:
                    status_response = requests.get(
                        f"http://127.0.0.1:8080/projects/{project_id}",
                        timeout=5
                    )
                    
                    if status_response.status_code == 200:
                        project_data = status_response.json()
                        project = project_data.get('data', {})
                        status = project.get('status', 'unknown')
                        
                        if status == 'Completed':
                            files = project.get('files', [])
                            print(f"✅ Project completed with {len(files)} files")
                            return True
                        elif status == 'Failed':
                            print(f"❌ Project failed: {project.get('output', 'Unknown error')}")
                            return False
                        else:
                            print(f"   Status: {status}")
                    
                except Exception as e:
                    print(f"   Error checking status: {e}")
            
            print("❌ Project generation timed out")
            return False
            
        else:
            print(f"❌ Backend generation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend generation test failed: {e}")
        return False


def test_tree_sitter_validation() -> bool:
    """Test Tree-Sitter validation"""
    print("\n🌳 Testing Tree-Sitter validation...")
    
    try:
        # Test JavaScript validation
        js_code = "const x = 1;\nconsole.log(x);"
        
        response = requests.post(
            "http://127.0.0.1:8000/validate",
            json={
                "language": "javascript",
                "code": js_code
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('valid', False):
                print("✅ JavaScript validation working")
            else:
                print("❌ JavaScript validation failed")
                print(f"   Errors: {data.get('errors', [])}")
                return False
        else:
            print(f"❌ Validation endpoint returned {response.status_code}")
            return False
        
        # Test TypeScript validation
        ts_code = "const x: number = 1;\nconsole.log(x);"
        
        response = requests.post(
            "http://127.0.0.1:8000/validate",
            json={
                "language": "typescript",
                "code": ts_code
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('valid', False):
                print("✅ TypeScript validation working")
                return True
            else:
                print("❌ TypeScript validation failed")
                print(f"   Errors: {data.get('errors', [])}")
                return False
        else:
            print(f"❌ Validation endpoint returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Tree-Sitter test failed: {e}")
        return False


def run_performance_test() -> Dict[str, Any]:
    """Run performance tests"""
    print("\n⚡ Running performance tests...")
    
    results = {
        "health_response_time": 0,
        "generation_response_time": 0,
        "memory_usage": "N/A"
    }
    
    # Test health endpoint response time
    try:
        start_time = time.time()
        response = requests.get("http://127.0.0.1:8000/health", timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            results["health_response_time"] = round((end_time - start_time) * 1000, 2)
            print(f"✅ Health response time: {results['health_response_time']}ms")
        else:
            print("❌ Health performance test failed")
    except Exception as e:
        print(f"❌ Health performance test error: {e}")
    
    # Test generation response time (simple prompt)
    try:
        start_time = time.time()
        response = requests.post(
            "http://127.0.0.1:8000/run",
            json={"prompt": "Create a simple variable", "backend": "ollama"},
            timeout=60
        )
        end_time = time.time()
        
        if response.status_code == 200:
            results["generation_response_time"] = round((end_time - start_time) * 1000, 2)
            print(f"✅ Generation response time: {results['generation_response_time']}ms")
        else:
            print("❌ Generation performance test failed")
    except Exception as e:
        print(f"❌ Generation performance test error: {e}")
    
    return results


def main():
    """Run comprehensive API tests"""
    print("🧪 Genesis API Test Suite")
    print("=" * 50)
    
    tests = [
        ("AI Core Health", test_health_endpoint),
        ("AI Core Root", test_root_endpoint),
        ("Project Generation", test_project_generation),
        ("Rust Backend Health", test_backend_health),
        ("Backend Generation", test_backend_generation),
        ("Tree-Sitter Validation", test_tree_sitter_validation),
    ]
    
    results = {}
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results[test_name] = success
            if success:
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Performance tests
    print(f"\n{'='*20} Performance Tests {'='*20}")
    performance_results = run_performance_test()
    
    # Summary
    print(f"\n{'='*20} Test Summary {'='*20}")
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    print("\nDetailed Results:")
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print("\nPerformance Results:")
    for metric, value in performance_results.items():
        print(f"  {metric}: {value}")
    
    if passed == total:
        print("\n🎉 All tests passed! Genesis is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 