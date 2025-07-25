#!/usr/bin/env python3
"""
MongoDB Setup and Testing Script for Genesis Project
Includes MongoDB Compass integration instructions
"""

import json
import subprocess
import sys
import time
from pathlib import Path
import requests

def check_mongodb_connection():
    """Check if MongoDB is running and accessible"""
    print("🔍 Checking MongoDB connection...")
    
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.server_info()  # Force connection
        print("✅ MongoDB is running and accessible")
        return True
    except ImportError:
        print("❌ PyMongo not installed. Install with: pip install pymongo")
        return False
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("   Make sure MongoDB is running on localhost:27017")
        return False

def test_backend_mongodb():
    """Test backend's MongoDB integration"""
    print("\n🧪 Testing Backend MongoDB Integration...")
    
    try:
        # Test backend health
        response = requests.get("http://localhost:8080/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            data = response.json()
            if data.get('success'):
                print(f"   Status: {data.get('message', 'Unknown')}")
            else:
                print(f"   Warning: {data}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
            
        # Test project creation
        print("\n📝 Testing project creation...")
        project_data = {
            "prompt": "Create a simple MongoDB test app",
            "backend": "ollama"
        }
        
        response = requests.post("http://localhost:8080/generate", 
                               json=project_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                project_id = result.get('data', {}).get('project_id', 'unknown')
                print(f"✅ Project created: {project_id}")
                return True
            else:
                print(f"❌ Project creation failed: {result.get('message')}")
        else:
            print(f"❌ Project creation request failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        print("   Make sure the backend is running on localhost:8080")
        
    return False

def print_mongodb_compass_instructions():
    """Print instructions for MongoDB Compass setup"""
    print("\n" + "="*60)
    print("📊 MONGODB COMPASS SETUP INSTRUCTIONS")
    print("="*60)
    print()
    print("MongoDB Compass is a GUI tool for viewing and managing MongoDB data.")
    print()
    print("🔗 Connection String:")
    print("   mongodb://localhost:27017/")
    print()
    print("📥 Download MongoDB Compass:")
    print("   https://www.mongodb.com/try/download/compass")
    print()
    print("⚙️  Setup Steps:")
    print("   1. Download and install MongoDB Compass")
    print("   2. Open MongoDB Compass")
    print("   3. In the connection screen, enter:")
    print("      Connection String: mongodb://localhost:27017/")
    print("   4. Click 'Connect'")
    print()
    print("🗂️  Expected Database Structure:")
    print("   Database: genesis")
    print("   Collection: projects")
    print()
    print("📋 Sample Document Structure:")
    sample_doc = {
        "_id": "ObjectId('...')",
        "project_id": "20240101_120000",
        "prompt": "Create a simple todo app",
        "files": [
            {
                "name": "package.json",
                "content": "{ ... }",
                "language": "json"
            }
        ],
        "output": "Successfully generated project",
        "status": "Completed",
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z",
        "backend": "ollama",
        "metadata": {}
    }
    print(json.dumps(sample_doc, indent=2))
    print()

def test_ai_core_direct():
    """Test AI Core directly"""
    print("\n🤖 Testing AI Core directly...")
    
    try:
        # Test health
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ AI Core is healthy")
        else:
            print(f"❌ AI Core health check failed: {response.status_code}")
            return False
            
        # Test generation
        print("📝 Testing file generation...")
        gen_data = {
            "prompt": "Create a simple MongoDB test component",
            "backend": "ollama"
        }
        
        response = requests.post("http://localhost:8000/run", 
                               json=gen_data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                data = result.get('data', {})
                files = data.get('files', [])
                print(f"✅ Generated {len(files)} files:")
                for file in files:
                    print(f"   - {file.get('name', 'unknown')} ({file.get('language', 'unknown')})")
                return True
            else:
                print(f"❌ Generation failed: {result.get('message')}")
        else:
            print(f"❌ Generation request failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ AI Core connection failed: {e}")
        print("   Make sure the AI Core is running on localhost:8000")
        
    return False

def check_service_status():
    """Check status of all services"""
    print("\n🔍 Checking Service Status...")
    print("-" * 40)
    
    services = {
        "MongoDB": ("localhost", 27017),
        "AI Core": ("localhost", 8000),
        "Backend": ("localhost", 8080)
    }
    
    for service, (host, port) in services.items():
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ {service}: Running on {host}:{port}")
            else:
                print(f"❌ {service}: Not accessible on {host}:{port}")
        except Exception as e:
            print(f"❌ {service}: Error checking - {e}")

def main():
    """Main setup and testing function"""
    print("🚀 Genesis MongoDB Setup & Testing")
    print("=" * 50)
    
    # Check service status
    check_service_status()
    
    # Check MongoDB
    mongodb_ok = check_mongodb_connection()
    
    # Test AI Core
    ai_core_ok = test_ai_core_direct()
    
    # Test Backend
    backend_ok = test_backend_mongodb()
    
    # Print MongoDB Compass instructions
    print_mongodb_compass_instructions()
    
    # Summary
    print("\n" + "="*60)
    print("📊 SETUP SUMMARY")
    print("="*60)
    print(f"MongoDB:    {'✅ Ready' if mongodb_ok else '❌ Issue'}")
    print(f"AI Core:    {'✅ Working' if ai_core_ok else '❌ Issue'}")
    print(f"Backend:    {'✅ Working' if backend_ok else '❌ Issue'}")
    print()
    
    if all([mongodb_ok, ai_core_ok, backend_ok]):
        print("🎉 All systems are operational!")
        print("   You can now use MongoDB Compass to view your project data.")
    else:
        print("⚠️  Some issues detected. Please check the details above.")
        print()
        print("🔧 Common fixes:")
        print("   - Start MongoDB: systemctl start mongod (Linux) or brew services start mongodb (Mac)")
        print("   - Start AI Core: cd ai_core && python main.py")
        print("   - Start Backend: cd backend && cargo run")
        print("   - Install dependencies: pip install pymongo requests")

if __name__ == "__main__":
    main() 