#!/usr/bin/env node

const Parser = require('tree-sitter');
const JavaScript = require('tree-sitter-javascript');
const TypeScript = require('tree-sitter-typescript');

// Language configurations
const LANGUAGES = {
    'javascript': {
        parser: JavaScript,
        extensions: ['.js', '.jsx'],
        name: 'JavaScript'
    },
    'typescript': {
        parser: TypeScript,
        extensions: ['.ts', '.tsx'],
        name: 'TypeScript'
    }
};

/**
 * Validate code using Tree-Sitter
 * @param {string} language - Programming language
 * @param {string} code - Source code to validate
 * @returns {Object} Validation results
 */
function validateCode(language, code) {
    const result = {
        valid: true,
        errors: [],
        warnings: [],
        language: language,
        timestamp: new Date().toISOString()
    };

    try {
        // Check if language is supported
        if (!LANGUAGES[language]) {
            result.valid = false;
            result.errors.push(`Unsupported language: ${language}`);
            return result;
        }

        // Create parser
        const parser = new Parser();
        const languageConfig = LANGUAGES[language];
        
        // Set language
        parser.setLanguage(languageConfig.parser);
        
        // Parse code
        const tree = parser.parse(code);
        
        // Check for syntax errors
        if (tree.rootNode.hasError()) {
            result.valid = false;
            result.errors.push('Syntax error detected');
            
            // Get detailed error information
            const errors = getParseErrors(tree.rootNode, code);
            result.errors.push(...errors);
        }
        
        // Additional validation rules
        const warnings = performAdditionalChecks(tree.rootNode, code, language);
        result.warnings.push(...warnings);
        
        // Add statistics
        result.statistics = {
            lines: code.split('\n').length,
            characters: code.length,
            nodes: countNodes(tree.rootNode)
        };

    } catch (error) {
        result.valid = false;
        result.errors.push(`Validation error: ${error.message}`);
    }

    return result;
}

/**
 * Get detailed parse errors from the syntax tree
 * @param {Object} node - Root node of the syntax tree
 * @param {string} code - Original source code
 * @returns {Array} Array of error messages
 */
function getParseErrors(node, code) {
    const errors = [];
    const lines = code.split('\n');
    
    function traverse(node) {
        if (node.type === 'ERROR') {
            const startLine = node.startPosition.row;
            const startColumn = node.startPosition.column;
            const endLine = node.endPosition.row;
            const endColumn = node.endPosition.column;
            
            let errorMessage = `Syntax error at line ${startLine + 1}, column ${startColumn + 1}`;
            
            // Add context line
            if (startLine < lines.length) {
                const contextLine = lines[startLine];
                errorMessage += `\nContext: ${contextLine}`;
                
                // Add pointer to error location
                if (startColumn < contextLine.length) {
                    const pointer = ' '.repeat(startColumn) + '^'.repeat(Math.max(1, endColumn - startColumn));
                    errorMessage += `\n         ${pointer}`;
                }
            }
            
            errors.push(errorMessage);
        }
        
        // Traverse children
        for (const child of node.children) {
            traverse(child);
        }
    }
    
    traverse(node);
    return errors;
}

/**
 * Perform additional code quality checks
 * @param {Object} node - Root node of the syntax tree
 * @param {string} code - Original source code
 * @param {string} language - Programming language
 * @returns {Array} Array of warning messages
 */
function performAdditionalChecks(node, code, language) {
    const warnings = [];
    
    // Check for common issues
    const lines = code.split('\n');
    
    // Check for long lines
    lines.forEach((line, index) => {
        if (line.length > 120) {
            warnings.push(`Line ${index + 1} is too long (${line.length} characters)`);
        }
    });
    
    // Check for trailing whitespace
    lines.forEach((line, index) => {
        if (line.endsWith(' ') || line.endsWith('\t')) {
            warnings.push(`Line ${index + 1} has trailing whitespace`);
        }
    });
    
    // Language-specific checks
    if (language === 'javascript' || language === 'typescript') {
        // Check for console.log statements (development code)
        if (code.includes('console.log(')) {
            warnings.push('Found console.log statements - consider removing for production');
        }
        
        // Check for TODO comments
        const todoRegex = /\/\/\s*TODO|\/\*\s*TODO/g;
        if (todoRegex.test(code)) {
            warnings.push('Found TODO comments - consider addressing before production');
        }
    }
    
    return warnings;
}

/**
 * Count nodes in the syntax tree
 * @param {Object} node - Root node
 * @returns {number} Number of nodes
 */
function countNodes(node) {
    let count = 1;
    for (const child of node.children) {
        count += countNodes(child);
    }
    return count;
}

/**
 * Main function for command line usage
 */
function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
        console.error('Usage: node validate.js <language> <code>');
        console.error('Example: node validate.js javascript "const x = 1;"');
        process.exit(1);
    }
    
    const language = args[0];
    const code = args[1];
    
    const result = validateCode(language, code);
    
    // Output JSON result
    console.log(JSON.stringify(result, null, 2));
    
    // Exit with appropriate code
    process.exit(result.valid ? 0 : 1);
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { validateCode, LANGUAGES };
}

// Run main function if called directly
if (require.main === module) {
    main();
} 