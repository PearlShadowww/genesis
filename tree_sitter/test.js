const { validateCode } = require('./validate.js');

console.log('🧪 Tree-Sitter Validation Test Suite');
console.log('=' * 40);

// Test cases
const testCases = [
    {
        name: 'Valid JavaScript',
        language: 'javascript',
        code: 'const x = 1;\nconsole.log(x);',
        shouldPass: true
    },
    {
        name: 'Invalid JavaScript',
        language: 'javascript',
        code: 'const x = 1\nconsole.log(x);', // Missing semicolon
        shouldPass: false
    },
    {
        name: 'Valid TypeScript',
        language: 'typescript',
        code: 'const x: number = 1;\nconsole.log(x);',
        shouldPass: true
    },
    {
        name: 'Invalid TypeScript',
        language: 'typescript',
        code: 'const x: number = "string";', // Type mismatch
        shouldPass: false
    },
    {
        name: 'Unsupported Language',
        language: 'python',
        code: 'x = 1',
        shouldPass: false
    }
];

let passed = 0;
let total = testCases.length;

testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. Testing: ${testCase.name}`);
    console.log(`Language: ${testCase.language}`);
    console.log(`Code: ${testCase.code}`);
    
    const result = validateCode(testCase.language, testCase.code);
    
    if (result.valid === testCase.shouldPass) {
        console.log('✅ PASS');
        passed++;
    } else {
        console.log('❌ FAIL');
        console.log(`Expected: ${testCase.shouldPass}, Got: ${result.valid}`);
        if (result.errors.length > 0) {
            console.log('Errors:', result.errors);
        }
    }
    
    if (result.warnings.length > 0) {
        console.log('⚠️  Warnings:', result.warnings);
    }
});

console.log(`\n📊 Test Results: ${passed}/${total} passed`);

if (passed === total) {
    console.log('🎉 All tests passed! Tree-Sitter validation is working correctly.');
} else {
    console.log('⚠️  Some tests failed. Check the output above.');
} 