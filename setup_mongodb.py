#!/usr/bin/env python3
"""
MongoDB Setup and Test Script for Genesis Project
"""

import requests
import json
import time
import subprocess
import sys
from typing import Dict, Any

def check_mongodb_connection():
    """Check if MongoDB is running and accessible"""
    try:
        # Try to connect to MongoDB using pymongo
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ MongoDB is running and accessible")
        return True
    except ImportError:
        print("⚠️  pymongo not installed. Install with: pip install pymongo")
        return False
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("💡 Make sure MongoDB is running on localhost:27017")
        return False

def test_backend_mongodb():
    """Test the backend with MongoDB integration"""
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8080/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend health check passed")
            print(f"   Services: {data.get('data', {}).get('services', {})}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
        
        # Test project generation
        print("\n🧪 Testing project generation with MongoDB...")
        project_data = {
            "prompt": "Create a simple React todo app with MongoDB integration",
            "backend": "ollama"
        }
        
        response = requests.post(
            "http://localhost:8080/generate",
            json=project_data,
            timeout=30
        )
        
        if response.status_code == 202:
            data = response.json()
            project_id = data.get("data")
            print(f"✅ Project generation started: {project_id}")
            
            # Wait for completion
            print("⏳ Waiting for project completion...")
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                
                status_response = requests.get(f"http://localhost:8080/projects/{project_id}", timeout=10)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    project = status_data.get("data", {})
                    status = project.get("status", "unknown")
                    files_count = len(project.get("files", []))
                    
                    print(f"📊 Status: {status}, Files: {files_count}")
                    
                    if status == "Completed" and files_count > 0:
                        print("🎉 Project completed successfully with MongoDB!")
                        return True
                    elif status == "Failed":
                        print("❌ Project generation failed")
                        return False
                else:
                    print(f"⚠️  Status check failed: {status_response.status_code}")
            
            print("⏰ Project generation timed out")
            return False
        else:
            print(f"❌ Project generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def setup_mongodb_compass():
    """Provide instructions for MongoDB Compass setup"""
    print("\n🗄️  MongoDB Compass Setup Instructions:")
    print("=" * 50)
    print("1. Download MongoDB Compass from: https://www.mongodb.com/try/download/compass")
    print("2. Install and open MongoDB Compass")
    print("3. Connect to: mongodb://localhost:27017")
    print("4. Create/select database: genesis")
    print("5. View collections: projects")
    print("6. You can now browse and query your generated projects!")
    print("\n📊 Example queries in Compass:")
    print("   - Find all projects: {}")
    print("   - Find completed projects: {status: 'Completed'}")
    print("   - Find recent projects: {created_at: {$gte: new Date('2024-01-01')}}")
    print("   - Find projects by prompt: {prompt: {$regex: 'todo', $options: 'i'}}")

def main():
    """Main setup function"""
    print("🚀 Genesis MongoDB Setup and Test")
    print("=" * 40)
    
    # Check MongoDB connection
    if not check_mongodb_connection():
        print("\n💡 To install MongoDB:")
        print("   Windows: Download from https://www.mongodb.com/try/download/community")
        print("   macOS: brew install mongodb-community")
        print("   Linux: sudo apt install mongodb")
        return
    
    # Test backend
    print("\n🔧 Testing backend with MongoDB...")
    if test_backend_mongodb():
        print("\n✅ All tests passed! MongoDB integration is working.")
    else:
        print("\n❌ Some tests failed. Check the backend logs.")
    
    # Setup instructions
    setup_mongodb_compass()
    
    print("\n🎉 Setup complete! You can now use MongoDB Compass to browse your projects.")

if __name__ == "__main__":
    main() 