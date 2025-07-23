#!/usr/bin/env python3
"""
Genesis Service Monitor
Monitors all Genesis services and provides health status
"""

import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class ServiceMonitor:
    """Monitor for Genesis services"""
    
    def __init__(self):
        self.services = {
            'frontend': {
                'url': 'http://localhost:5173',
                'name': 'Tauri Frontend',
                'port': 5173
            },
            'backend': {
                'url': 'http://localhost:8080',
                'name': 'Rust Backend',
                'port': 8080
            },
            'ai_core': {
                'url': 'http://localhost:8000',
                'name': 'Python AI Core',
                'port': 8000
            },
            'ollama': {
                'url': 'http://localhost:11434',
                'name': 'Ollama LLM',
                'port': 11434
            }
        }
        
        self.health_data = {}
    
    async def check_service_health(self, session: aiohttp.ClientSession, service_key: str, service_info: Dict) -> Dict:
        """Check health of a specific service"""
        start_time = time.time()
        
        try:
            # Check if port is open
            port_open = await self.check_port(service_info['port'])
            
            if not port_open:
                return {
                    'status': 'down',
                    'response_time': None,
                    'error': 'Port not accessible',
                    'last_check': datetime.now().isoformat()
                }
            
            # Try HTTP health check
            try:
                async with session.get(f"{service_info['url']}/health", timeout=5) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'healthy',
                            'response_time': response_time,
                            'data': data,
                            'last_check': datetime.now().isoformat()
                        }
                    else:
                        return {
                            'status': 'unhealthy',
                            'response_time': response_time,
                            'error': f'HTTP {response.status}',
                            'last_check': datetime.now().isoformat()
                        }
            
            except aiohttp.ClientError as e:
                return {
                    'status': 'unhealthy',
                    'response_time': time.time() - start_time,
                    'error': str(e),
                    'last_check': datetime.now().isoformat()
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'response_time': time.time() - start_time,
                'error': str(e),
                'last_check': datetime.now().isoformat()
            }
    
    async def check_port(self, port: int) -> bool:
        """Check if a port is open"""
        try:
            # Use asyncio to check port
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection('localhost', port),
                timeout=2.0
            )
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False
    
    async def check_system_resources(self) -> Dict:
        """Check system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': disk.percent,
                'disk_free_gb': disk.free / (1024**3)
            }
        except Exception as e:
            logger.error(f"Error checking system resources: {e}")
            return {}
    
    async def monitor_all_services(self) -> Dict:
        """Monitor all services"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for service_key, service_info in self.services.items():
                task = self.check_service_health(session, service_key, service_info)
                tasks.append((service_key, task))
            
            # Execute all health checks concurrently
            results = {}
            for service_key, task in tasks:
                results[service_key] = await task
            
            # Add system resources
            results['system'] = await self.check_system_resources()
            
            return results
    
    def print_status(self, health_data: Dict):
        """Print formatted status"""
        print("\n" + "="*60)
        print(f"Genesis Service Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Service status
        for service_key, service_info in self.services.items():
            if service_key in health_data:
                status = health_data[service_key]
                status_icon = {
                    'healthy': '✅',
                    'unhealthy': '⚠️',
                    'down': '❌',
                    'error': '💥'
                }.get(status['status'], '❓')
                
                response_time = status.get('response_time')
                response_str = f"({response_time:.3f}s)" if response_time else ""
                
                print(f"{status_icon} {service_info['name']:<20} {status['status']:<10} {response_str}")
                
                if 'error' in status:
                    print(f"    Error: {status['error']}")
        
        # System resources
        if 'system' in health_data:
            sys_info = health_data['system']
            print(f"\n💻 System Resources:")
            print(f"   CPU: {sys_info.get('cpu_percent', 0):.1f}%")
            print(f"   Memory: {sys_info.get('memory_percent', 0):.1f}% ({sys_info.get('memory_available_gb', 0):.1f}GB free)")
            print(f"   Disk: {sys_info.get('disk_percent', 0):.1f}% ({sys_info.get('disk_free_gb', 0):.1f}GB free)")
        
        print("="*60)
    
    async def continuous_monitor(self, interval: int = 30):
        """Continuously monitor services"""
        logger.info(f"Starting continuous monitoring (interval: {interval}s)")
        
        while True:
            try:
                health_data = await self.monitor_all_services()
                self.print_status(health_data)
                
                # Save to file
                with open('monitor_log.json', 'w') as f:
                    json.dump(health_data, f, indent=2)
                
                await asyncio.sleep(interval)
            
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(interval)

async def main():
    """Main function"""
    monitor = ServiceMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        await monitor.continuous_monitor()
    else:
        # Single check
        health_data = await monitor.monitor_all_services()
        monitor.print_status(health_data)

if __name__ == "__main__":
    asyncio.run(main()) 