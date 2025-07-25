#!/usr/bin/env python3
"""
Simple Backend-AI Core Connection Test
"""

import requests
import json
import time

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get("http://localhost:8080/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is healthy")
            print(f"   AI Core status: {data.get('data', {}).get('services', {}).get('ai_core', 'unknown')}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_project_generation():
    """Test project generation flow"""
    try:
        # Send generation request
        request_data = {
            "prompt": "Create a simple todo app",
            "backend": "ollama"
        }
        
        print("🧪 Testing project generation...")
        response = requests.post(
            "http://localhost:8080/generate",
            json=request_data,
            timeout=30
        )
        
        if response.status_code == 202:  # Accepted
            data = response.json()
            project_id = data.get("data")
            print(f"✅ Project generation started: {project_id}")
            
            # Wait and check status
            time.sleep(3)
            
            status_response = requests.get(f"http://localhost:8080/projects/{project_id}", timeout=10)
            if status_response.status_code == 200:
                status_data = status_response.json()
                project_status = status_data.get("data", {}).get("status", "unknown")
                files_count = len(status_data.get("data", {}).get("files", []))
                
                print(f"📊 Project status: {project_status}")
                print(f"📊 Files generated: {files_count}")
                
                if project_status == "Completed" and files_count > 0:
                    print("🎉 Real AI generation working!")
                    return True
                elif project_status == "Failed":
                    print("❌ Project generation failed")
                    return False
                else:
                    print("⚠️  Project still generating or no files")
                    return False
            else:
                print(f"❌ Failed to get project status: {status_response.status_code}")
                return False
        else:
            print(f"❌ Project generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Project generation test failed: {e}")
        return False

def main():
    """Run connection tests"""
    print("🔍 Simple Backend-AI Core Connection Test")
    print("=" * 50)
    
    # Test backend health
    backend_ok = test_backend_health()
    
    if backend_ok:
        # Test project generation
        generation_ok = test_project_generation()
        
        print("\n" + "=" * 50)
        print("📋 Test Summary:")
        print(f"   Backend Health: {'✅' if backend_ok else '❌'}")
        print(f"   Project Generation: {'✅' if generation_ok else '❌'}")
        
        if backend_ok and generation_ok:
            print("\n🎉 Backend-AI Core connection is working!")
            print("   The frontend should now show real generated files instead of mock data.")
        else:
            print("\n⚠️  Some issues remain. Check the details above.")
    else:
        print("\n❌ Backend is not accessible. Please start the backend first.")

if __name__ == "__main__":
    main() 