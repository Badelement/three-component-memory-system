#!/usr/bin/env python3
"""
Diagnostic script for Three-Component Memory System.
"""

import sys
import os
import json
import platform

def diagnose():
    """Run comprehensive diagnostics."""
    print("🔍 Three-Component Memory System - Diagnostic Report")
    print("=" * 60)
    
    # System information
    print("\n📊 System Information:")
    print(f"  Python: {sys.version}")
    print(f"  Platform: {platform.platform()}")
    print(f"  Processor: {platform.processor()}")
    
    # Check dependencies
    print("\n📦 Dependencies:")
    dependencies = ['lancedb', 'networkx', 'sentence_transformers', 'numpy']
    
    for dep in dependencies:
        try:
            module = __import__(dep.replace('_', '-') if dep == 'sentence_transformers' else dep)
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✅ {dep}: {version}")
        except ImportError:
            print(f"  ❌ {dep}: Not installed")
    
    # Check source files
    print("\n📁 Source Files:")
    src_files = ['__init__.py', 'memory_core.py']
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    
    for file in src_files:
        file_path = os.path.join(src_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✅ {file}: {size} bytes")
        else:
            print(f"  ❌ {file}: Missing")
    
    # Test import
    print("\n🧪 Import Test:")
    try:
        sys.path.insert(0, src_path)
        from three_component_memory import MemorySystem, __version__
        print(f"  ✅ Import successful (v{__version__})")
        
        # Test initialization
        import tempfile
        test_dir = tempfile.mkdtemp()
        
        try:
            memory = MemorySystem({'data_path': test_dir, 'debug': False})
            print("  ✅ System initialization successful")
            
            # Test basic operations
            stats = memory.get_stats()
            print(f"  ✅ System status: {stats.get('status', 'unknown')}")
            
            # Test add
            memory_id = memory.add("Diagnostic test memory", category="diagnostic")
            if memory_id:
                print(f"  ✅ Memory addition successful: {memory_id}")
            else:
                print("  ⚠️  Memory addition returned None")
            
            # Test search
            results = memory.search("diagnostic", search_type="text")
            print(f"  ✅ Search found {len(results)} results")
            
        finally:
            import shutil
            shutil.rmtree(test_dir)
            
    except Exception as e:
        print(f"  ❌ Import/Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Check data directory
    print("\n📂 Data Directory:")
    data_dir = os.path.expanduser('~/.openclaw/memory/three_component')
    if os.path.exists(data_dir):
        print(f"  ✅ Exists: {data_dir}")
        
        # Check contents
        try:
            items = os.listdir(data_dir)
            print(f"  ✅ Contains: {len(items)} items")
            for item in items[:5]:  # Show first 5 items
                item_path = os.path.join(data_dir, item)
                if os.path.isdir(item_path):
                    print(f"    📁 {item}/")
                else:
                    size = os.path.getsize(item_path)
                    print(f"    📄 {item} ({size} bytes)")
            if len(items) > 5:
                print(f"    ... and {len(items) - 5} more")
        except:
            print("  ⚠️  Cannot list contents")
    else:
        print(f"  ⚠️  Does not exist (will be created on first use)")
    
    # OpenClaw integration check
    print("\n🔗 OpenClaw Integration:")
    config_path = os.path.expanduser('~/.openclaw/config.json')
    if os.path.exists(config_path):
        print(f"  ✅ Config file exists: {config_path}")
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            skill_config = config.get('skills', {}).get('three-component-memory', {})
            if skill_config:
                print(f"  ✅ Skill configured:")
                for key, value in skill_config.items():
                    print(f"    • {key}: {value}")
            else:
                print("  ⚠️  Skill not configured in config.json")
        except Exception as e:
            print(f"  ❌ Cannot read config: {e}")
    else:
        print("  ⚠️  OpenClaw config not found")
    
    print("\n" + "=" * 60)
    print("🎉 Diagnostic complete!")
    print("\n💡 Recommendations:")
    
    issues = []
    if not all(__import__(dep.replace('_', '-') if dep == 'sentence_transformers' else dep, fromlist=['']) for dep in dependencies):
        issues.append("Install missing dependencies: pip install lancedb networkx sentence-transformers numpy")
    
    if not os.path.exists(src_path):
        issues.append("Source directory not found")
    
    if issues:
        print("\n⚠️  Issues found:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("  ✅ No major issues found")
    
    print("\n📞 For help:")
    print("  • Check docs/troubleshooting.md")
    print("  • Run examples/basic_usage.py")
    print("  • Open an issue on GitHub")

if __name__ == "__main__":
    diagnose()
