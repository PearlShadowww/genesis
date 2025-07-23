import logging
from typing import Dict, Any
from tree_sitter_tools import validate_code_tool, validate_files_tool

logger = logging.getLogger(__name__)

def validate_code(language: str, code: str) -> Dict[str, Any]:
    """
    Validate code using Tree-Sitter
    
    Args:
        language: Programming language (javascript, typescript, dart)
        code: Source code to validate
    
    Returns:
        Dictionary with validation results
    """
    try:
        return validate_code_tool(language, code)
    except Exception as e:
        logger.error(f"Code validation failed: {e}")
        return {
            "valid": False,
            "errors": [str(e)],
            "language": language
        }

def validate_multiple_files(files: list) -> Dict[str, Any]:
    """
    Validate multiple code files
    
    Args:
        files: List of file dictionaries with 'name', 'content', 'language'
    
    Returns:
        Dictionary with validation results for all files
    """
    try:
        results = validate_files_tool(files)
        
        # Aggregate results
        all_valid = all(result.get('valid', False) for result in results)
        all_errors = []
        all_warnings = []
        
        for result in results:
            all_errors.extend(result.get('errors', []))
            all_warnings.extend(result.get('warnings', []))
        
        return {
            "valid": all_valid,
            "errors": all_errors,
            "warnings": all_warnings,
            "file_results": results,
            "total_files": len(files)
        }
        
    except Exception as e:
        logger.error(f"Multiple file validation failed: {e}")
        return {
            "valid": False,
            "errors": [str(e)],
            "file_results": [],
            "total_files": len(files)
        } 