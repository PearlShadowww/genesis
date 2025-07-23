#!/usr/bin/env python3
"""
Test LLM with CrewAI integration
"""

from llm import get_llm
from crewai import Agent, Task, Crew

def test_simple_llm():
    """Test LLM directly"""
    print("🧪 Testing LLM directly...")
    try:
        llm = get_llm()
        response = llm.invoke("Write a simple JavaScript function that adds two numbers")
        print(f"✅ LLM response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False

def test_simple_agent():
    """Test simple agent with LLM"""
    print("\n🧪 Testing simple agent...")
    try:
        llm = get_llm()
        
        agent = Agent(
            role="Test Developer",
            goal="Write simple code examples",
            backstory="You are a helpful developer",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
        
        task = Task(
            description="Write a simple JavaScript function that adds two numbers",
            expected_output="A JavaScript function"
        )
        
        task.agent = agent
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        print(f"✅ Agent test completed: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run tests"""
    print("🔍 LLM CrewAI Debug Test")
    print("=" * 40)
    
    test_simple_llm()
    test_simple_agent()

if __name__ == "__main__":
    main() 