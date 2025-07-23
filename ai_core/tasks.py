from crewai import Task
import logging

logger = logging.getLogger(__name__)

def create_tasks(prompt: str):
    """Create CrewAI tasks for project generation"""
    
    # Task 1: Plan the project
    plan_task = Task(
        description=f"""
        Analyze the following project request and create a detailed plan:
        
        REQUEST: {prompt}
        
        Create a comprehensive project plan that includes:
        1. Project structure and file organization
        2. Required dependencies and packages
        3. Key components and their responsibilities
        4. Data flow and state management
        5. User interface design considerations
        6. Testing strategy
        
        Format your response as a structured JSON plan that can be easily
        understood and implemented by the development team.
        """,
        expected_output="""
        A detailed JSON project plan with:
        - project_name: string
        - description: string
        - structure: object with file paths and descriptions
        - dependencies: array of required packages
        - components: array of component descriptions
        - features: array of feature descriptions
        """
    )
    
    # Task 2: Generate code
    code_task = Task(
        description="""
        Based on the project plan created by the architect, generate all
        necessary code files for the software project.
        
        Ensure your code:
        1. Follows best practices and coding standards
        2. Is well-documented with comments
        3. Includes proper error handling
        4. Is modular and maintainable
        5. Implements all specified features
        
        Generate each file with proper syntax highlighting and file extensions.
        """,
        expected_output="""
        Complete code files for the project, including:
        - Package configuration files (package.json, pubspec.yaml, etc.)
        - Source code files with proper extensions
        - Configuration files
        - Documentation files
        
        Each file should be clearly marked with its path and language.
        """,
        context=[plan_task]
    )
    
    # Task 3: Debug and validate
    debug_task = Task(
        description="""
        Review the generated code for:
        1. Syntax errors and bugs
        2. Code quality issues
        3. Security vulnerabilities
        4. Performance optimizations
        5. Best practice violations
        
        Provide specific fixes and improvements for any issues found.
        """,
        expected_output="""
        A comprehensive code review report with:
        - List of issues found
        - Specific fixes and improvements
        - Final validated code files
        - Quality assessment score
        """,
        context=[code_task]
    )
    
    return [plan_task, code_task, debug_task] 