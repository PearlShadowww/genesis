#!/usr/bin/env python3
"""
Complete System Integration Test
Tests backend, AI core, MongoDB integration, and file generation
"""

import requests
import json
import time
import sys
from datetime import datetime

def test_service_health():
    """Test all service health endpoints"""
    print("🏥 Testing Service Health...")
    print("-" * 50)
    
    services = {
        "Backend": "http://localhost:8080/health",
        "AI Core": "http://localhost:8000/health"
    }
    
    all_healthy = True
    
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ {service}: Healthy")
                    if service == "Backend":
                        ai_status = data.get('data', {}).get('ai_core_health', 'unknown')
                        print(f"   AI Core status from backend: {ai_status}")
                else:
                    print(f"⚠️  {service}: Response not successful - {data}")
                    all_healthy = False
            else:
                print(f"❌ {service}: HTTP {response.status_code}")
                all_healthy = False
        except Exception as e:
            print(f"❌ {service}: Connection failed - {e}")
            all_healthy = False
    
    return all_healthy

def test_ai_core_generation():
    """Test AI Core file generation directly"""
    print("\n🤖 Testing AI Core Generation...")
    print("-" * 50)
    
    try:
        gen_request = {
            "prompt": "Create a simple React calculator app with add, subtract, multiply, and divide functions",
            "backend": "ollama"
        }
        
        print(f"📝 Prompt: {gen_request['prompt'][:60]}...")
        print("⏳ Generating files (this may take 30-60 seconds)...")
        
        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/run", 
            json=gen_request, 
            timeout=120
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                data = result.get('data', {})
                files = data.get('files', [])
                output = data.get('output', '')
                
                print(f"✅ Generation successful in {end_time - start_time:.1f} seconds")
                print(f"📁 Generated {len(files)} files:")
                
                for file in files:
                    name = file.get('name', 'unknown')
                    language = file.get('language', 'unknown')
                    content_size = len(file.get('content', ''))
                    print(f"   - {name} ({language}) - {content_size} chars")
                
                print(f"📄 Output: {output[:100]}...")
                return True, files
            else:
                print(f"❌ Generation failed: {result.get('message')}")
                return False, []
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
            return False, []
            
    except Exception as e:
        print(f"❌ AI Core generation failed: {e}")
        return False, []

def test_backend_integration():
    """Test backend integration with AI core"""
    print("\n🔗 Testing Backend Integration...")
    print("-" * 50)
    
    try:
        # Test project generation through backend
        project_request = {
            "prompt": "Create a simple todo list application with React and TypeScript",
            "backend": "ollama"
        }
        
        print(f"📝 Prompt: {project_request['prompt'][:60]}...")
        print("⏳ Starting project generation through backend...")
        
        start_time = time.time()
        response = requests.post(
            "http://localhost:8080/generate", 
            json=project_request, 
            timeout=30
        )
        
        if response.status_code in [200, 202]:  # Accept both OK and Accepted
            result = response.json()
            if result.get('success'):
                project_id = result.get('data')
                print(f"✅ Project generation started: {project_id}")
                
                # Wait and check project status
                print("⏳ Waiting for generation to complete...")
                for i in range(12):  # Wait up to 60 seconds
                    time.sleep(5)
                    status_response = requests.get(f"http://localhost:8080/projects/{project_id}")
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        if status_data.get('success'):
                            project = status_data.get('data', {})
                            status = project.get('status', 'unknown')
                            files = project.get('files', [])
                            
                            print(f"📊 Status check {i+1}: {status} - {len(files)} files")
                            
                            if status == "Completed":
                                end_time = time.time()
                                print(f"✅ Project completed in {end_time - start_time:.1f} seconds")
                                print(f"📁 Final files generated: {len(files)}")
                                
                                for file in files:
                                    name = file.get('name', 'unknown')
                                    language = file.get('language', 'unknown')
                                    print(f"   - {name} ({language})")
                                
                                return True, project_id
                            elif status == "Failed":
                                print(f"❌ Project generation failed")
                                return False, project_id
                
                print("⚠️  Project still generating after 60 seconds")
                return False, project_id
            else:
                print(f"❌ Failed to start generation: {result.get('message')}")
                return False, None
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
            return False, None
            
    except Exception as e:
        print(f"❌ Backend integration test failed: {e}")
        return False, None

def test_project_listing():
    """Test project listing functionality"""
    print("\n📋 Testing Project Listing...")
    print("-" * 50)
    
    try:
        response = requests.get("http://localhost:8080/projects", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                projects = result.get('data', [])
                print(f"✅ Retrieved {len(projects)} projects")
                
                for project in projects[:3]:  # Show first 3 projects
                    project_id = project.get('project_id', 'unknown')
                    status = project.get('status', 'unknown')
                    files_count = len(project.get('files', []))
                    created = project.get('created_at', 'unknown')
                    prompt = project.get('prompt', '')[:50]
                    
                    print(f"   📁 {project_id}: {status} - {files_count} files")
                    print(f"      Created: {created}")
                    print(f"      Prompt: {prompt}...")
                
                return True
            else:
                print(f"❌ Failed to list projects: {result.get('message')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Project listing test failed: {e}")
        return False

def run_complete_test():
    """Run all tests and provide summary"""
    print("🚀 GENESIS COMPLETE SYSTEM TEST")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Service Health
    results['health'] = test_service_health()
    
    # Test 2: AI Core Generation
    results['ai_generation'], generated_files = test_ai_core_generation()
    
    # Test 3: Backend Integration
    results['backend_integration'], project_id = test_backend_integration()
    
    # Test 4: Project Listing
    results['project_listing'] = test_project_listing()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        test_display = test_name.replace('_', ' ').title()
        print(f"{test_display:20} {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! System is fully operational!")
        print("\n✅ Ready for production use:")
        print("   - MongoDB Compass: mongodb://localhost:27017/")
        print("   - Backend API: http://localhost:8080")
        print("   - AI Core: http://localhost:8000")
    else:
        print("⚠️  Some tests failed. Please check the details above.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_complete_test() 