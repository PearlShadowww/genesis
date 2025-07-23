#!/usr/bin/env python3
"""
Test script to verify Genesis optimizations
"""

import os
import json
from pathlib import Path

def test_python_optimizations():
    """Test Python optimizations"""
    print("🧪 Testing Python optimizations...")
    
    # Test orjson availability
    try:
        import orjson
        print("✅ orjson available for fast JSON parsing")
    except ImportError:
        print("❌ orjson not available")
    
    # Test gunicorn availability
    try:
        import gunicorn
        print("✅ gunicorn available for production server")
    except ImportError:
        print("❌ gunicorn not available")

def test_rust_optimizations():
    """Test Rust optimizations"""
    print("\n🧪 Testing Rust optimizations...")
    
    cargo_toml = Path("backend/Cargo.toml")
    if cargo_toml.exists():
        with open(cargo_toml, 'r') as f:
            content = f.read()
            
        optimizations = [
            ("opt-level = 3", "Maximum optimization level"),
            ("lto = true", "Link Time Optimization"),
            ("strip = true", "Debug symbol stripping")
        ]
        
        for opt, desc in optimizations:
            if opt in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc} - not found")

def test_frontend_optimizations():
    """Test frontend optimizations"""
    print("\n🧪 Testing frontend optimizations...")
    
    # Test package.json scripts
    package_json = Path("genesis-frontend/package.json")
    if package_json.exists():
        with open(package_json, 'r') as f:
            data = json.load(f)
            
        scripts = data.get("scripts", {})
        required_scripts = [
            "dev:optimized",
            "build:optimized", 
            "analyze"
        ]
        
        for script in required_scripts:
            if script in scripts:
                print(f"✅ {script} script available")
            else:
                print(f"❌ {script} script not found")

def test_startup_scripts():
    """Test optimized startup scripts"""
    print("\n🧪 Testing startup scripts...")
    
    scripts = [
        ("start_optimized.bat", "Windows optimized startup"),
        ("start_optimized.sh", "Linux/Mac optimized startup")
    ]
    
    for script_path, desc in scripts:
        script = Path(script_path)
        if script.exists():
            print(f"✅ {desc} script available")
        else:
            print(f"❌ {desc} script not found")

def main():
    """Run all optimization tests"""
    print("🚀 Genesis Optimization Test Suite")
    print("=" * 50)
    
    test_python_optimizations()
    test_rust_optimizations()
    test_frontend_optimizations()
    test_startup_scripts()
    
    print("\n" + "=" * 50)
    print("🎉 Optimization testing complete!")
    print("\n📊 Next steps:")
    print("1. Install new dependencies: pip install -r ai_core/requirements.txt")
    print("2. Test optimized startup: ./start_optimized.sh (or .bat)")
    print("3. Build optimized: npm run build:optimized && cargo build --release")

if __name__ == "__main__":
    main() 