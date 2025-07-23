#!/usr/bin/env python3
"""
Simple debug script to test AI core functionality
"""

import requests
from llm import get_llm
from agents import create_agents
from tasks import create_tasks

def test_llm():
    """Test LLM initialization"""
    print("🧪 Testing LLM initialization...")
    try:
        llm = get_llm()
        print("✅ LLM initialized successfully")
        return True
    except Exception as e:
        print(f"❌ LLM initialization failed: {e}")
        return False

def test_agents():
    """Test agent creation"""
    print("\n🧪 Testing agent creation...")
    try:
        llm = get_llm()
        agents = create_agents(llm)
        print(f"✅ Created {len(agents)} agents successfully")
        return True
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_tasks():
    """Test task creation"""
    print("\n🧪 Testing task creation...")
    try:
        tasks = create_tasks("Create a simple React counter component")
        print(f"✅ Created {len(tasks)} tasks successfully")
        return True
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        return False

def test_crew():
    """Test crew execution"""
    print("\n🧪 Testing crew execution...")
    try:
        from models import Prompt
        from crewai import Crew
        
        # Create components
        llm = get_llm()
        agents = create_agents(llm)
        tasks = create_tasks("Create a simple React counter component")
        
        # Assign agents to tasks
        tasks[0].agent = agents[0]  # Planner task -> Planner agent
        tasks[1].agent = agents[1]  # Code task -> Coder agent
        tasks[2].agent = agents[2]  # Debug task -> Debugger agent
        
        # Create crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True
        )
        
        # Run crew
        result = crew.kickoff()
        print("✅ Crew execution completed")
        print(f"Result: {result}")
        return True
    except Exception as e:
        print(f"❌ Crew execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoint():
    """Test API endpoint directly"""
    print("\n🧪 Testing API endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/run",
            json={
                "prompt": "Create a simple React counter component",
                "backend": "ollama"
            },
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ API endpoint test passed")
            return True
        else:
            print("❌ API endpoint test failed")
            return False
            
    except Exception as e:
        print(f"❌ API endpoint test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Genesis AI Core Debug Test")
    print("=" * 40)
    
    tests = [
        ("LLM", test_llm),
        ("Agents", test_agents),
        ("Tasks", test_tasks),
        ("Crew", test_crew),
        ("API Endpoint", test_api_endpoint)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    print("\n📊 Test Results:")
    print("=" * 40)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n🎯 Overall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main() 