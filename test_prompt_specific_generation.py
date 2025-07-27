#!/usr/bin/env python3
"""
Test script to verify LLM generates files specific to prompts in separate folders
Tests different project types and ensures each gets its own folder with appropriate files
"""

import requests
import time
import json
import os
from pathlib import Path
from datetime import datetime

def test_react_project():
    """Test React project generation"""
    print("🔍 Testing React project generation...")
    
    prompt = "Create a React todo app with add, delete, and mark complete functionality"
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/run',
            json={
                "prompt": prompt,
                "backend": "ollama"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            files = data.get('data', {}).get('files', [])
            project_path = data.get('data', {}).get('project_path', '')
            
            print(f"✅ React project generated successfully")
            print(f"   📁 Project path: {project_path}")
            print(f"   📄 Generated {len(files)} files:")
            
            file_names = [f.get('name', '') for f in files]
            for file in files:
                print(f"      - {file.get('name')} ({file.get('language')})")
            
            # Check for React-specific files
            has_package_json = 'package.json' in file_names
            has_react_files = any('.js' in name or '.jsx' in name or '.tsx' in name for name in file_names)
            has_html = any('.html' in name for name in file_names)
            has_readme = any('readme' in name.lower() for name in file_names)
            
            print(f"   ✅ Package.json: {has_package_json}")
            print(f"   ✅ React files: {has_react_files}")
            print(f"   ✅ HTML files: {has_html}")
            print(f"   ✅ README: {has_readme}")
            
            # Check if folder exists
            if project_path and os.path.exists(project_path):
                print(f"   ✅ Project folder exists on disk")
                return True
            else:
                print(f"   ❌ Project folder not found")
                return False
        else:
            print(f"❌ React project generation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ React project test error: {e}")
        return False

def test_python_project():
    """Test Python project generation"""
    print("\n🔍 Testing Python project generation...")
    
    prompt = "Create a Python web scraper that extracts data from websites"
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/run',
            json={
                "prompt": prompt,
                "backend": "ollama"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            files = data.get('data', {}).get('files', [])
            project_path = data.get('data', {}).get('project_path', '')
            
            print(f"✅ Python project generated successfully")
            print(f"   📁 Project path: {project_path}")
            print(f"   📄 Generated {len(files)} files:")
            
            file_names = [f.get('name', '') for f in files]
            for file in files:
                print(f"      - {file.get('name')} ({file.get('language')})")
            
            # Check for Python-specific files
            has_python_files = any('.py' in name for name in file_names)
            has_requirements = 'requirements.txt' in file_names
            has_readme = any('readme' in name.lower() for name in file_names)
            has_gitignore = '.gitignore' in file_names
            
            print(f"   ✅ Python files: {has_python_files}")
            print(f"   ✅ Requirements.txt: {has_requirements}")
            print(f"   ✅ README: {has_readme}")
            print(f"   ✅ .gitignore: {has_gitignore}")
            
            # Check if folder exists
            if project_path and os.path.exists(project_path):
                print(f"   ✅ Project folder exists on disk")
                return True
            else:
                print(f"   ❌ Project folder not found")
                return False
        else:
            print(f"❌ Python project generation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Python project test error: {e}")
        return False

def test_node_project():
    """Test Node.js project generation"""
    print("\n🔍 Testing Node.js project generation...")
    
    prompt = "Create a Node.js Express API server with user authentication"
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/run',
            json={
                "prompt": prompt,
                "backend": "ollama"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            files = data.get('data', {}).get('files', [])
            project_path = data.get('data', {}).get('project_path', '')
            
            print(f"✅ Node.js project generated successfully")
            print(f"   📁 Project path: {project_path}")
            print(f"   📄 Generated {len(files)} files:")
            
            file_names = [f.get('name', '') for f in files]
            for file in files:
                print(f"      - {file.get('name')} ({file.get('language')})")
            
            # Check for Node.js-specific files
            has_package_json = 'package.json' in file_names
            has_js_files = any('.js' in name for name in file_names)
            has_readme = any('readme' in name.lower() for name in file_names)
            has_env_example = '.env.example' in file_names or '.env' in file_names
            
            print(f"   ✅ Package.json: {has_package_json}")
            print(f"   ✅ JavaScript files: {has_js_files}")
            print(f"   ✅ README: {has_readme}")
            print(f"   ✅ Environment files: {has_env_example}")
            
            # Check if folder exists
            if project_path and os.path.exists(project_path):
                print(f"   ✅ Project folder exists on disk")
                return True
            else:
                print(f"   ❌ Project folder not found")
                return False
        else:
            print(f"❌ Node.js project generation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Node.js project test error: {e}")
        return False

def check_separate_folders():
    """Check that different projects are in separate folders"""
    print("\n🔍 Checking separate folder creation...")
    
    documents_dir = Path.home() / "Documents"
    genesis_dir = documents_dir / "genesis"
    
    if not genesis_dir.exists():
        print("❌ Genesis directory not found")
        return False
    
    # List all project folders
    project_folders = [f for f in genesis_dir.iterdir() if f.is_dir()]
    
    if len(project_folders) >= 3:
        print(f"✅ Found {len(project_folders)} project folders:")
        for folder in project_folders:
            print(f"   📁 {folder.name}")
        
        # Check that folders are different
        folder_names = [f.name for f in project_folders]
        unique_folders = set(folder_names)
        
        if len(unique_folders) == len(folder_names):
            print("✅ All projects are in separate folders")
            return True
        else:
            print("❌ Some projects share the same folder")
            return False
    else:
        print(f"❌ Not enough project folders found: {len(project_folders)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Prompt-Specific Project Generation Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test different project types
    tests = [
        ("React Project", test_react_project),
        ("Python Project", test_python_project),
        ("Node.js Project", test_node_project),
        ("Separate Folders", check_separate_folders),
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
        print("🎉 All tests passed! LLM generates prompt-specific files in separate folders.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the services and try again.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main()) 