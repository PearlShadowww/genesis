"""
Tree-Sitter integration tools for the AI core
"""

import subprocess
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class TreeSitterValidator:
    """Tree-Sitter code validation wrapper"""
    
    def __init__(self, tree_sitter_path: str = "../tree_sitter"):
        self.tree_sitter_path = Path(tree_sitter_path)
        self.validate_script = self.tree_sitter_path / "validate.js"
        
        if not self.validate_script.exists():
            raise FileNotFoundError(f"Tree-Sitter validation script not found: {self.validate_script}")
    
    def validate_code(self, language: str, code: str) -> Dict[str, Any]:
        """
        Validate code using Tree-Sitter
        
        Args:
            language: Programming language (javascript, typescript)
            code: Source code to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Prepare the command
            cmd = [
                "node", 
                str(self.validate_script), 
                language, 
                code
            ]
            
            # Run validation
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.tree_sitter_path
            )
            
            if result.returncode == 0:
                # Parse JSON output
                validation_result = json.loads(result.stdout)
                logger.info(f"Code validation completed for {language}")
                return validation_result
            else:
                logger.error(f"Tree-Sitter validation failed: {result.stderr}")
                return {
                    "valid": False,
                    "errors": [f"Validation process failed: {result.stderr}"],
                    "language": language
                }
                
        except subprocess.TimeoutExpired:
            logger.error("Tree-Sitter validation timed out")
            return {
                "valid": False,
                "errors": ["Validation timeout"],
                "language": language
            }
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Tree-Sitter output: {e}")
            return {
                "valid": False,
                "errors": [f"Invalid validation output: {e}"],
                "language": language
            }
        except Exception as e:
            logger.error(f"Tree-Sitter validation error: {e}")
            return {
                "valid": False,
                "errors": [str(e)],
                "language": language
            }
    
    def validate_file(self, file_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a code file
        
        Args:
            file_path: Path to the file to validate
            language: Programming language (auto-detected if None)
            
        Returns:
            Dictionary with validation results
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {
                    "valid": False,
                    "errors": [f"File not found: {file_path}"],
                    "language": language or "unknown"
                }
            
            # Auto-detect language if not provided
            if language is None:
                language = self._detect_language(file_path)
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            return self.validate_code(language, code)
            
        except Exception as e:
            logger.error(f"File validation error: {e}")
            return {
                "valid": False,
                "errors": [str(e)],
                "language": language or "unknown"
            }
    
    def _detect_language(self, file_path: Path) -> str:
        """Auto-detect programming language from file extension"""
        extension = file_path.suffix.lower()
        
        language_map = {
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.mjs': 'javascript',
            '.cjs': 'javascript'
        }
        
        return language_map.get(extension, 'javascript')
    
    def batch_validate(self, files: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Validate multiple files
        
        Args:
            files: List of dicts with 'name', 'content', 'language' keys
            
        Returns:
            List of validation results
        """
        results = []
        
        for file_info in files:
            result = self.validate_code(
                file_info['language'],
                file_info['content']
            )
            result['file_name'] = file_info['name']
            results.append(result)
        
        return results

# Global validator instance
validator = TreeSitterValidator()

def validate_code_tool(language: str, code: str) -> Dict[str, Any]:
    """
    Tool function for CrewAI integration
    
    Args:
        language: Programming language
        code: Source code to validate
        
    Returns:
        Validation results
    """
    return validator.validate_code(language, code)

def validate_files_tool(files: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Tool function for batch validation
    
    Args:
        files: List of files to validate
        
    Returns:
        List of validation results
    """
    return validator.batch_validate(files) 