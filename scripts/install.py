#!/usr/bin/env python3
"""
Installation script for three-component memory system
Follows skill-creator standards for scripts/
"""

import sys
import subprocess
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required Python packages"""
    packages = [
        "lancedb>=0.29.0",
        "networkx>=3.6.0", 
        "sentence-transformers>=2.2.0",
        "numpy>=1.24.0"
    ]
    
    print("📦 Installing dependencies...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✅ {package}")
        except subprocess.CalledProcessError:
            print(f"  ❌ Failed to install {package}")
            return False
    
    return True

def create_data_directory():
    """Create data directory"""
    data_dir = os.path.expanduser("~/.openclaw/memory/three_component")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(os.path.join(data_dir, "lancedb"), exist_ok=True)
    os.makedirs(os.path.join(data_dir, "graph"), exist_ok=True)
    
    print(f"📁 Created data directory: {data_dir}")
    return True

def verify_installation():
    """Verify installation"""
    print("🔍 Verifying installation...")
    
    test_imports = [
        ("lancedb", "lancedb"),
        ("networkx", "networkx"),
        ("sentence_transformers", "sentence_transformers"),
    ]
    
    all_ok = True
    for name, module in test_imports:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name}")
            all_ok = False
    
    return all_ok

def main():
    """Main installation function"""
    print("🔧 Installing Three-Component Memory System")
    print("=" * 50)
    
    steps = [
        ("Python version check", check_python_version),
        ("Install dependencies", install_dependencies),
        ("Create data directory", create_data_directory),
        ("Verify installation", verify_installation)
    ]
    
    all_passed = True
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ {step_name} failed")
            all_passed = False
            break
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Installation completed successfully!")
        print("\nNext steps:")
        print("1. Copy skill to OpenClaw: cp -r . ~/.openclaw/skills/three-component-memory")
        print("2. Test: python -c \"from three_component_memory import MemorySystem; m=MemorySystem(); print(m.get_stats())\"")
        print("3. Use in OpenClaw conversations")
    else:
        print("❌ Installation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
