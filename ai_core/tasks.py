from crewai import Task
import logging

logger = logging.getLogger(__name__)

def create_tasks(prompt: str):
    """Create CrewAI tasks for project generation"""
    
    # Task 1: Plan the project
    plan_task = Task(
        description=f"Create a simple project plan for: {prompt}. Include basic file structure and dependencies.",
        expected_output="A simple project plan with file structure and dependencies"
    )
    
    # Task 2: Generate code
    code_task = Task(
        description=f"Generate code files for: {prompt}. Create the main application files.",
        expected_output="Code files for the application"
    )
    
    # Task 3: Review and improve
    review_task = Task(
        description=f"Review and improve the code for: {prompt}. Fix any issues and add improvements.",
        expected_output="Improved code files with fixes and enhancements"
    )
    
    return [plan_task, code_task, review_task] 