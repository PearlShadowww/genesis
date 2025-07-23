#!/usr/bin/env node

/**
 * Test script to verify frontend-backend connection for Genesis
 */

const http = require('http');

// Test endpoints
const endpoints = [
  { name: 'AI Core Health', url: 'http://127.0.0.1:8000/health' },
  { name: 'AI Core Root', url: 'http://127.0.0.1:8000/' },
  { name: 'Frontend Dev Server', url: 'http://localhost:5173' }
];

function testEndpoint(endpoint) {
  return new Promise((resolve) => {
    const url = new URL(endpoint.url);
    
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: 'GET',
      timeout: 5000
    };

    const req = http.request(options, (res) => {
      resolve({
        name: endpoint.name,
        status: res.statusCode,
        success: res.statusCode >= 200 && res.statusCode < 300
      });
    });

    req.on('error', () => {
      resolve({
        name: endpoint.name,
        status: 'CONN_ERROR',
        success: false
      });
    });

    req.on('timeout', () => {
      resolve({
        name: endpoint.name,
        status: 'TIMEOUT',
        success: false
      });
    });

    req.end();
  });
}

async function testConnection() {
  console.log('🧪 Genesis Frontend-Backend Connection Test');
  console.log('=' * 50);
  
  const results = await Promise.all(endpoints.map(testEndpoint));
  
  console.log('\n📊 Results:');
  results.forEach(result => {
    const icon = result.success ? '✅' : '❌';
    console.log(`${icon} ${result.name}: ${result.status}`);
  });
  
  const allConnected = results.every(r => r.success);
  
  console.log('\n📝 Summary:');
  if (allConnected) {
    console.log('🎉 All services are running and connected!');
    console.log('You can now test project generation in the frontend.');
  } else {
    console.log('⚠️  Some services are not running. Please check:');
    
    if (!results[0].success) {
      console.log('- Start AI Core: cd ai_core && uvicorn main:app --host 127.0.0.1 --port 8000');
    }
    if (!results[2].success) {
      console.log('- Start Frontend: cd genesis-frontend && npm run dev');
    }
  }
  
  console.log('\n🔗 Test API Call:');
  console.log('curl -X POST http://127.0.0.1:8000/run \\');
  console.log('  -H "Content-Type: application/json" \\');
  console.log('  -d \'{"prompt": "Create a simple React component", "backend": "ollama"}\'');
}

if (require.main === module) {
  testConnection().catch(console.error);
} 