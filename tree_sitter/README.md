# Genesis Tree-Sitter Validation

Node.js module for code syntax validation using Tree-Sitter.

## Features
- Syntax validation for JavaScript and TypeScript
- Detailed error reporting with line numbers and context
- Code quality warnings
- Batch file validation
- Integration with Python AI core

## Supported Languages
- JavaScript (.js, .jsx, .mjs, .cjs)
- TypeScript (.ts, .tsx)

## Setup
```bash
cd tree_sitter
npm install
```

## Usage

### Command Line
```bash
# Validate JavaScript code
node validate.js javascript "const x = 1;"

# Validate TypeScript code
node validate.js typescript "const x: number = 1;"
```

### Programmatic Usage
```javascript
const { validateCode } = require('./validate.js');

const result = validateCode('javascript', 'const x = 1;');
console.log(result);
```

### Python Integration
```python
from tree_sitter_tools import TreeSitterValidator

validator = TreeSitterValidator()
result = validator.validate_code('javascript', 'const x = 1;')
```

## Output Format
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "language": "javascript",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "statistics": {
    "lines": 1,
    "characters": 12,
    "nodes": 5
  }
}
```

## Testing
```bash
npm test
```

## Integration
The Tree-Sitter module integrates with the Genesis AI core to validate generated code before returning it to users. 