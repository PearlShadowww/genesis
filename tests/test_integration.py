#!/usr/bin/env python3
"""
Integration tests for Genesis AI-powered software generator
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Any

import aiohttp
import pytest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenesisIntegrationTest:
    """Integration test suite for Genesis"""
    
    def __init__(self):
        self.base_urls = {
            'frontend': 'http://localhost:5173',
            'backend': 'http://localhost:8080',
            'ai_core': 'http://localhost:8000',
            'ollama': 'http://localhost:11434'
        }
        self.session = None
    
    async def setup(self):
        """Setup test environment"""
        self.session = aiohttp.ClientSession()
        logger.info("Integration test setup complete")
    
    async def teardown(self):
        """Cleanup test environment"""
        if self.session:
            await self.session.close()
        logger.info("Integration test teardown complete")
    
    async def test_service_connectivity(self) -> Dict[str, bool]:
        """Test basic connectivity to all services"""
        results = {}
        
        for service_name, url in self.base_urls.items():
            try:
                # Try to connect to each service
                if service_name == 'ollama':
                    # Ollama doesn't have a health endpoint, check tags
                    async with self.session.get(f"{url}/api/tags", timeout=5) as response:
                        results[service_name] = response.status == 200
                else:
                    # Other services should have health endpoints
                    async with self.session.get(f"{url}/health", timeout=5) as response:
                        results[service_name] = response.status == 200
                
                logger.info(f"✅ {service_name}: {'Connected' if results[service_name] else 'Failed'}")
                
            except Exception as e:
                results[service_name] = False
                logger.error(f"❌ {service_name}: Connection failed - {e}")
        
        return results
    
    async def test_backend_health_endpoint(self) -> Dict[str, Any]:
        """Test backend health endpoint"""
        try:
            async with self.session.get(f"{self.base_urls['backend']}/health", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ Backend health check passed")
                    return {'success': True, 'data': data}
                else:
                    logger.error(f"❌ Backend health check failed: HTTP {response.status}")
                    return {'success': False, 'error': f'HTTP {response.status}'}
        
        except Exception as e:
            logger.error(f"❌ Backend health check error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def test_ai_core_health_endpoint(self) -> Dict[str, Any]:
        """Test AI core health endpoint"""
        try:
            async with self.session.get(f"{self.base_urls['ai_core']}/health", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ AI Core health check passed")
                    return {'success': True, 'data': data}
                else:
                    logger.error(f"❌ AI Core health check failed: HTTP {response.status}")
                    return {'success': False, 'error': f'HTTP {response.status}'}
        
        except Exception as e:
            logger.error(f"❌ AI Core health check error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def test_ollama_models(self) -> Dict[str, Any]:
        """Test Ollama model availability"""
        try:
            async with self.session.get(f"{self.base_urls['ollama']}/api/tags", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get('models', [])
                    
                    # Check for required models
                    required_models = ['qwen2.5-coder:1.5b-base', 'llama3.1:8b']
                    available_models = [model['name'] for model in models]
                    
                    missing_models = [model for model in required_models 
                                    if not any(model in name for name in available_models)]
                    
                    if missing_models:
                        logger.warning(f"⚠️ Missing models: {missing_models}")
                        return {
                            'success': False,
                            'error': f'Missing models: {missing_models}',
                            'available': available_models
                        }
                    else:
                        logger.info(f"✅ All required models available: {available_models}")
                        return {
                            'success': True,
                            'models': available_models
                        }
                else:
                    logger.error(f"❌ Ollama API failed: HTTP {response.status}")
                    return {'success': False, 'error': f'HTTP {response.status}'}
        
        except Exception as e:
            logger.error(f"❌ Ollama API error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def test_project_generation_flow(self) -> Dict[str, Any]:
        """Test complete project generation flow"""
        test_prompt = "Create a simple React counter component with increment and decrement buttons"
        
        try:
            # Step 1: Send generation request to backend
            generation_request = {
                'prompt': test_prompt,
                'backend': 'ollama'
            }
            
            logger.info("🚀 Testing project generation flow...")
            logger.info(f"📝 Test prompt: {test_prompt}")
            
            async with self.session.post(
                f"{self.base_urls['backend']}/generate",
                json=generation_request,
                timeout=30
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"❌ Generation request failed: HTTP {response.status}")
                    logger.error(f"Error: {error_text}")
                    return {'success': False, 'error': f'HTTP {response.status}: {error_text}'}
                
                data = await response.json()
                logger.info("✅ Generation request accepted")
                
                if not data.get('success'):
                    logger.error(f"❌ Generation failed: {data.get('message', 'Unknown error')}")
                    return {'success': False, 'error': data.get('message', 'Unknown error')}
                
                project_id = data.get('data')
                logger.info(f"📋 Project ID: {project_id}")
                
                # Step 2: Poll for project completion
                max_attempts = 60  # 5 minutes with 5-second intervals
                for attempt in range(max_attempts):
                    await asyncio.sleep(5)
                    
                    try:
                        async with self.session.get(
                            f"{self.base_urls['backend']}/projects/{project_id}",
                            timeout=10
                        ) as status_response:
                            
                            if status_response.status == 200:
                                project_data = await status_response.json()
                                
                                if project_data.get('success') and project_data.get('data'):
                                    project = project_data['data']
                                    status = project.get('status', 'Unknown')
                                    
                                    logger.info(f"📊 Project status: {status}")
                                    
                                    if status == 'Completed':
                                        files = project.get('files', [])
                                        logger.info(f"✅ Project completed! Generated {len(files)} files")
                                        return {
                                            'success': True,
                                            'project_id': project_id,
                                            'files_count': len(files),
                                            'files': files
                                        }
                                    
                                    elif status == 'Failed':
                                        error_msg = project.get('output', 'Unknown error')
                                        logger.error(f"❌ Project failed: {error_msg}")
                                        return {'success': False, 'error': error_msg}
                                    
                                    # Still processing, continue polling
                                    continue
                            
                            logger.warning(f"⚠️ Status check failed: HTTP {status_response.status}")
                    
                    except Exception as e:
                        logger.warning(f"⚠️ Status check error: {e}")
                
                # Timeout
                logger.error("❌ Project generation timed out")
                return {'success': False, 'error': 'Generation timed out'}
        
        except Exception as e:
            logger.error(f"❌ Generation flow error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling with invalid requests"""
        test_cases = [
            {
                'name': 'Empty prompt',
                'request': {'prompt': '', 'backend': 'ollama'},
                'expected_error': 'Prompt cannot be empty'
            },
            {
                'name': 'Invalid backend',
                'request': {'prompt': 'Test prompt', 'backend': 'invalid'},
                'expected_error': 'Invalid backend'
            },
            {
                'name': 'Missing prompt',
                'request': {'backend': 'ollama'},
                'expected_error': 'Missing prompt'
            }
        ]
        
        results = {}
        
        for test_case in test_cases:
            try:
                async with self.session.post(
                    f"{self.base_urls['backend']}/generate",
                    json=test_case['request'],
                    timeout=10
                ) as response:
                    
                    if response.status == 400:
                        data = await response.json()
                        error_msg = data.get('message', '')
                        
                        if test_case['expected_error'].lower() in error_msg.lower():
                            results[test_case['name']] = True
                            logger.info(f"✅ {test_case['name']}: Error handled correctly")
                        else:
                            results[test_case['name']] = False
                            logger.warning(f"⚠️ {test_case['name']}: Unexpected error message")
                    else:
                        results[test_case['name']] = False
                        logger.error(f"❌ {test_case['name']}: Expected 400, got {response.status}")
            
            except Exception as e:
                results[test_case['name']] = False
                logger.error(f"❌ {test_case['name']}: Test error - {e}")
        
        return results
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("🧪 Starting Genesis Integration Tests")
        logger.info("=" * 50)
        
        await self.setup()
        
        try:
            results = {
                'connectivity': await self.test_service_connectivity(),
                'backend_health': await self.test_backend_health_endpoint(),
                'ai_core_health': await self.test_ai_core_health_endpoint(),
                'ollama_models': await self.test_ollama_models(),
                'error_handling': await self.test_error_handling(),
                'generation_flow': await self.test_project_generation_flow()
            }
            
            # Summary
            logger.info("\n" + "=" * 50)
            logger.info("📊 Integration Test Summary")
            logger.info("=" * 50)
            
            total_tests = 0
            passed_tests = 0
            
            for test_name, result in results.items():
                if isinstance(result, dict):
                    if result.get('success', False):
                        logger.info(f"✅ {test_name}: PASSED")
                        passed_tests += 1
                    else:
                        logger.error(f"❌ {test_name}: FAILED - {result.get('error', 'Unknown error')}")
                    total_tests += 1
                elif isinstance(result, dict) and 'connectivity' in test_name:
                    for service, connected in result.items():
                        if connected:
                            logger.info(f"✅ {service}: Connected")
                            passed_tests += 1
                        else:
                            logger.error(f"❌ {service}: Not connected")
                        total_tests += 1
            
            logger.info(f"\n🎯 Results: {passed_tests}/{total_tests} tests passed")
            
            if passed_tests == total_tests:
                logger.info("🎉 All integration tests passed!")
            else:
                logger.warning("⚠️ Some tests failed. Check the logs above.")
            
            return results
        
        finally:
            await self.teardown()

async def main():
    """Main function to run integration tests"""
    tester = GenesisIntegrationTest()
    results = await tester.run_all_tests()
    
    # Save results to file
    with open('integration_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Exit with appropriate code
    if results.get('generation_flow', {}).get('success', False):
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    asyncio.run(main()) 