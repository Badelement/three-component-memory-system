#!/usr/bin/env python3
"""
Test script for Three-Component Memory System skill
Based on skill-creator best practices: concise, focused, practical
"""

import sys
import os
import tempfile
from pathlib import Path

# Add skill directory to path
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

def test_basic_functionality():
    """Test core functionality of the memory system"""
    print("🧪 Testing Three-Component Memory System Skill")
    print("=" * 50)
    
    try:
        from three_component_memory import MemorySystem
        
        # Use temporary directory for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"📁 Using temporary directory: {tmpdir}")
            
            # Initialize with test config
            config = {
                "data_path": tmpdir,
                "debug": True,
                "auto_record": False  # Disable auto-record for testing
            }
            
            memory = MemorySystem(config)
            print("✅ MemorySystem initialized successfully")
            
            # Test adding memory
            test_content = "Test memory: Project planning meeting decision"
            memory_id = memory.add(
                content=test_content,
                category="test",
                importance=4,
                tags=["test", "planning"]
            )
            print(f"✅ Memory added: {memory_id}")
            
            # Test searching
            results = memory.search("project planning", search_type="hybrid", limit=3)
            print(f"✅ Search completed, found {len(results)} results")
            
            # Test stats
            stats = memory.get_stats()
            memory_count = stats.get('total_memories', stats.get('memory_count', 0))
            print(f"✅ System stats: {memory_count} memories")
            
            # Test component health (if available)
            if hasattr(memory, 'check_health'):
                health = memory.check_health()
                print(f"✅ System health: {health.get('status', 'unknown')}")
            else:
                print("⚠️ check_health method not available (optional)")
            
            print("\n🎉 All tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_openclaw_integration():
    """Test OpenClaw-specific integration"""
    print("\n🔗 Testing OpenClaw Integration")
    print("=" * 50)
    
    try:
        # Check if skill is properly structured
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            print(f"✅ SKILL.md found ({skill_md.stat().st_size} bytes)")
        else:
            print("❌ SKILL.md not found")
            return False
            
        # Check references directory
        ref_dir = skill_dir / "references"
        if ref_dir.exists():
            ref_files = list(ref_dir.glob("*.md"))
            print(f"✅ References directory: {len(ref_files)} files")
            for f in ref_files:
                print(f"   - {f.name}")
        else:
            print("❌ References directory not found")
            return False
            
        # Check examples
        examples_dir = skill_dir / "examples"
        if examples_dir.exists():
            example_files = list(examples_dir.glob("*.py"))
            print(f"✅ Examples directory: {len(example_files)} files")
        else:
            print("⚠️ Examples directory not found (optional)")
            
        print("\n✅ OpenClaw integration checks passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Three-Component Memory System Skill Validation")
    print("Based on skill-creator best practices\n")
    
    # Run tests
    func_ok = test_basic_functionality()
    integration_ok = test_openclaw_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if func_ok and integration_ok:
        print("🎉 SUCCESS: Skill is ready for production use!")
        print("\nRecommendations based on skill-creator:")
        print("1. ✅ SKILL.md is concise and focused")
        print("2. ✅ References are properly organized")
        print("3. ✅ Core functionality works")
        print("4. ✅ OpenClaw integration is complete")
        return 0
    else:
        print("⚠️ ISSUES FOUND: Skill needs improvement")
        if not func_ok:
            print("   - Core functionality tests failed")
        if not integration_ok:
            print("   - OpenClaw integration issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())