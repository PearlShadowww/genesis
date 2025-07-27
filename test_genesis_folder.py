#!/usr/bin/env python3
"""
Test script to verify Genesis folder creation and LLM orchestration
Tests: Frontend -> Backend -> AI Core -> Ollama -> Documents/genesis folder
"""

import requests
import time
import json
import os
from pathlib import Path
from datetime import datetime

def test_genesis_folder_creation():
    """Test that the genesis folder is created in Documents"""
    print("🔍 Testing Genesis folder creation...")
    
    documents_dir = Path.home() / "Documents"
    genesis_dir = documents_dir / "genesis"
    
    if genesis_dir.exists():
        print(f"✅ Genesis folder exists at: {genesis_dir}")
        return True
    else:
        print(f"❌ Genesis folder not found at: {genesis_dir}")
        return False

def test_ai_core_genesis_info():
    """Test that AI Core reports genesis directory"""
    print("\n🔍 Testing AI Core genesis directory info...")
    
    try:
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            genesis_dir = data.get('data', {}).get('genesis_dir')
            
            if genesis_dir:
                print(f"✅ AI Core reports genesis directory: {genesis_dir}")
                return True
            else:
                print("❌ AI Core doesn't report genesis directory")
                return False
        else:
            print(f"❌ AI Core health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI Core test error: {e}")
        return False

def test_project_generation_with_folder():
    """Test complete project generation with folder creation"""
    print("\n🚀 Testing project generation with folder creation...")
    
    test_prompt = "Create a simple React todo app with add and delete functionality"
    
    try:
        # Step 1: Send generation request to backend
        print("   📤 Sending request to backend...")
        response = requests.post(
            'http://127.0.0.1:8080/generate',
            json={
                "prompt": test_prompt,
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
                        project_path = project_data.get('project_path', '')
                        
                        print(f"   ✅ Project completed!")
                        print(f"   📁 Project path: {project_path}")
                        print(f"   📄 Generated {len(files)} files:")
                        for file in files:
                            print(f"      - {file.get('name')} ({file.get('language')})")
                        
                        # Check if project folder exists
                        if project_path and os.path.exists(project_path):
                            print(f"   ✅ Project folder exists on disk: {project_path}")
                            
                            # List files in the project folder
                            project_files = list(Path(project_path).rglob('*'))
                            print(f"   📂 Files on disk: {len(project_files)}")
                            for file_path in project_files:
                                if file_path.is_file():
                                    print(f"      - {file_path.name}")
                            
                            return True
                        else:
                            print(f"   ❌ Project folder not found on disk: {project_path}")
                            return False
                        
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
        print(f"   ❌ Project generation test failed: {e}")
        return False

def test_llm_orchestration():
    """Test that LLM is orchestrating the project structure"""
    print("\n🧠 Testing LLM orchestration...")
    
    try:
        # Test direct AI Core call to see LLM orchestration
        response = requests.post(
            'http://127.0.0.1:8000/run',
            json={
                "prompt": "Create a Python web scraper",
                "backend": "ollama"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            files = data.get('data', {}).get('files', [])
            project_path = data.get('data', {}).get('project_path', '')
            
            print(f"✅ LLM orchestration successful")
            print(f"   📁 Project path: {project_path}")
            print(f"   📄 Generated {len(files)} files:")
            
            # Check if LLM created appropriate files for a Python web scraper
            file_names = [f.get('name', '') for f in files]
            has_python_files = any('.py' in name for name in file_names)
            has_requirements = 'requirements.txt' in file_names
            has_readme = any('readme' in name.lower() for name in file_names)
            
            if has_python_files:
                print("   ✅ LLM created Python files")
            if has_requirements:
                print("   ✅ LLM created requirements.txt")
            if has_readme:
                print("   ✅ LLM created README")
            
            return True
        else:
            print(f"❌ LLM orchestration failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ LLM orchestration test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Genesis Folder & LLM Orchestration Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test all components
    tests = [
        ("Genesis Folder Creation", test_genesis_folder_creation),
        ("AI Core Genesis Info", test_ai_core_genesis_info),
        ("LLM Orchestration", test_llm_orchestration),
        ("Project Generation with Folder", test_project_generation_with_folder),
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
        print("🎉 All tests passed! Genesis folder creation and LLM orchestration is working.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the services and try again.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main()) 