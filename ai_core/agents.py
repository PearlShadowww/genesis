from crewai import Agent
import logging

logger = logging.getLogger(__name__)

def create_agents(llm):
    """Create CrewAI agents for software development"""
    
    # Planner Agent - Creates project plans
    planner = Agent(
        role="Software Architect",
        goal="Create detailed project plans and architecture for software projects",
        backstory="""You are an experienced software architect with expertise in 
        React, Flutter, and Electron development. You excel at breaking down 
        complex requirements into clear, implementable plans.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[]
    )
    
    # Coder Agent - Generates code files
    coder = Agent(
        role="Senior Software Developer",
        goal="Generate high-quality, production-ready code based on project plans",
        backstory="""You are a senior software developer with 10+ years of experience
        in React, TypeScript, Flutter, and Electron. You write clean, maintainable
        code and follow best practices.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[]
    )
    
    # Debugger Agent - Analyzes and fixes code
    debugger = Agent(
        role="Code Quality Specialist",
        goal="Analyze generated code for errors, bugs, and improvements",
        backstory="""You are a code quality specialist with expertise in static
        analysis, testing, and debugging. You ensure code meets high standards
        and follows best practices.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[]
    )
    
    return [planner, coder, debugger] 