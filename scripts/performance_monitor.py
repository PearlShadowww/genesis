#!/usr/bin/env python3
"""
Performance Monitor for Genesis
Monitors system resources and service performance
"""

import psutil
import time
import platform
import requests
from datetime import datetime
from pathlib import Path

class GenesisPerformanceMonitor:
    def __init__(self):
        self.services = {
            "ollama": "http://localhost:11434/api/tags",
            "ai_core": "http://localhost:8000/health",
            "backend": "http://localhost:8080/health",
            "frontend": "http://localhost:5173"
        }
        
    def get_system_stats(self):
        """Get system resource statistics"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "disk_percent": psutil.disk_usage('/').percent if platform.system() != "Windows" else psutil.disk_usage('C:\\').percent
        }
    
    def get_service_status(self):
        """Check status of Genesis services"""
        status = {}
        
        for service_name, url in self.services.items():
            try:
                response = requests.get(url, timeout=2)
                status[service_name] = {
                    "status": "running" if response.status_code == 200 else "error",
                    "response_time": round(response.elapsed.total_seconds() * 1000, 2),
                    "status_code": response.status_code
                }
            except requests.exceptions.RequestException:
                status[service_name] = {
                    "status": "down",
                    "response_time": None,
                    "status_code": None
                }
                
        return status
    
    def get_process_stats(self):
        """Get statistics for Genesis-related processes"""
        processes = {}
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
            try:
                proc_info = proc.info
                name = proc_info['name'].lower()
                
                # Check for Genesis-related processes
                if any(keyword in name for keyword in ['python', 'cargo', 'node', 'ollama']):
                    processes[name] = {
                        "pid": proc_info['pid'],
                        "cpu_percent": proc_info['cpu_percent'],
                        "memory_percent": proc_info['memory_percent'],
                        "memory_mb": round(proc_info['memory_info'].rss / (1024**2), 2)
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return processes
    
    def display_stats(self):
        """Display current statistics"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Get statistics
        system_stats = self.get_system_stats()
        service_status = self.get_service_status()
        process_stats = self.get_process_stats()
        
        # Clear screen (works on most terminals)
        print("\033[2J\033[H", end="")
        
        print("📊 Genesis Performance Monitor")
        print("=" * 50)
        print(f"Time: {timestamp}")
        print()
        
        # System stats
        print("🖥️  System Resources:")
        print(f"  CPU: {system_stats['cpu_percent']:5.1f}% | "
              f"Memory: {system_stats['memory_percent']:5.1f}% ({system_stats['memory_available_gb']:.1f}GB free) | "
              f"Disk: {system_stats['disk_percent']:5.1f}%")
        print()
        
        # Service status
        print("🌐 Service Status:")
        for service, info in service_status.items():
            status_icon = "✅" if info['status'] == 'running' else "❌"
            response_time = f"{info['response_time']}ms" if info['response_time'] else "N/A"
            print(f"  {status_icon} {service:12} | {info['status']:8} | {response_time:>8}")
        print()
        
        # Process stats
        if process_stats:
            print("⚙️  Process Statistics:")
            for proc_name, info in process_stats.items():
                print(f"  📦 {proc_name:15} | CPU: {info['cpu_percent']:5.1f}% | "
                      f"Memory: {info['memory_percent']:5.1f}% ({info['memory_mb']:6.1f}MB)")
        else:
            print("⚙️  Process Statistics: No Genesis processes found")
        print()
        
        # Performance recommendations
        self.display_recommendations(system_stats, service_status, process_stats)
    
    def display_recommendations(self, system_stats, service_status, process_stats):
        """Display performance recommendations"""
        recommendations = []
        
        # CPU recommendations
        if system_stats['cpu_percent'] > 80:
            recommendations.append("⚠️  High CPU usage - consider reducing load")
        elif system_stats['cpu_percent'] > 60:
            recommendations.append("📈 Moderate CPU usage - system is working well")
        else:
            recommendations.append("✅ Low CPU usage - system has capacity")
        
        # Memory recommendations
        if system_stats['memory_percent'] > 90:
            recommendations.append("🚨 Critical memory usage - restart services")
        elif system_stats['memory_percent'] > 80:
            recommendations.append("⚠️  High memory usage - monitor closely")
        elif system_stats['memory_percent'] > 60:
            recommendations.append("📈 Moderate memory usage - normal operation")
        else:
            recommendations.append("✅ Low memory usage - system has capacity")
        
        # Service recommendations
        down_services = [name for name, info in service_status.items() if info['status'] == 'down']
        if down_services:
            recommendations.append(f"❌ Services down: {', '.join(down_services)}")
        
        # Process recommendations
        high_cpu_processes = [name for name, info in process_stats.items() if info['cpu_percent'] > 50]
        if high_cpu_processes:
            recommendations.append(f"🔥 High CPU processes: {', '.join(high_cpu_processes)}")
        
        print("💡 Recommendations:")
        for rec in recommendations:
            print(f"  {rec}")
    
    def run_monitor(self, interval=5):
        """Run the performance monitor"""
        print("🚀 Starting Genesis Performance Monitor...")
        print("Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                self.display_stats()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Performance monitor stopped")

def main():
    """Main function"""
    monitor = GenesisPerformanceMonitor()
    monitor.run_monitor()

if __name__ == "__main__":
    main() 