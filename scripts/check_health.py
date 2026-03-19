#!/usr/bin/env python3
"""
Health check script for Three-Component Memory System.
Run this to diagnose issues or verify the system is working.
"""

import os
import sys
import json
from pathlib import Path

def check_health():
    """Run comprehensive health checks."""
    results = {
        "status": "healthy",
        "checks": [],
        "issues": [],
        "recommendations": []
    }
    
    # Add skill directory to path
    skill_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(skill_dir))
    
    try:
        from three_component_memory import MemorySystem
        from three_component_memory.memory_core import MemoryCore
        
        # Check 1: Can import modules
        results["checks"].append({
            "name": "import_modules",
            "status": "passed",
            "message": "Successfully imported memory modules"
        })
        
        # Check 2: Initialize memory system
        try:
            memory = MemorySystem()
            results["checks"].append({
                "name": "initialize_system",
                "status": "passed",
                "message": "Memory system initialized successfully"
            })
            
            # Check 3: Get configuration
            config = memory.get_config()
            results["checks"].append({
                "name": "get_configuration",
                "status": "passed",
                "message": f"Configuration loaded: {len(config)} settings"
            })
            
            # Check 4: Get statistics
            stats = memory.get_stats()
            results["checks"].append({
                "name": "get_statistics",
                "status": "passed",
                "message": f"Statistics: {stats.get('memory_count', 0)} memories"
            })
            
            # Check 5: Test search (if there are memories)
            if stats.get('memory_count', 0) > 0:
                try:
                    test_results = memory.search("test", limit=1)
                    results["checks"].append({
                        "name": "test_search",
                        "status": "passed",
                        "message": f"Search test completed: {len(test_results)} results"
                    })
                except Exception as e:
                    results["checks"].append({
                        "name": "test_search",
                        "status": "failed",
                        "message": f"Search test failed: {str(e)}"
                    })
                    results["issues"].append("Search functionality may be impaired")
            
            # Check 6: Storage locations
            storage_path = Path.home() / ".openclaw" / "memory" / "three_component"
            if storage_path.exists():
                results["checks"].append({
                    "name": "storage_exists",
                    "status": "passed",
                    "message": f"Storage directory exists: {storage_path}"
                })
                
                # Check subdirectories
                subdirs = ["lancedb", "graph"]
                for subdir in subdirs:
                    subdir_path = storage_path / subdir
                    if subdir_path.exists():
                        results["checks"].append({
                            "name": f"subdir_{subdir}",
                            "status": "passed",
                            "message": f"{subdir} directory exists"
                        })
                    else:
                        results["checks"].append({
                            "name": f"subdir_{subdir}",
                            "status": "warning",
                            "message": f"{subdir} directory missing (may be first run)"
                        })
            else:
                results["checks"].append({
                    "name": "storage_exists",
                    "status": "warning",
                    "message": "Storage directory doesn't exist (may be first run)"
                })
            
            # Check 7: Configuration values
            required_settings = ["enabled", "auto_record", "importance_threshold"]
            for setting in required_settings:
                if setting in config:
                    results["checks"].append({
                        "name": f"config_{setting}",
                        "status": "passed",
                        "message": f"{setting}: {config[setting]}"
                    })
                else:
                    results["checks"].append({
                        "name": f"config_{setting}",
                        "status": "warning",
                        "message": f"Missing configuration: {setting}"
                    })
            
            # Generate recommendations
            if config.get("auto_record") is False:
                results["recommendations"].append("Enable auto_record to automatically save important conversations")
            
            if config.get("importance_threshold", 3) > 3:
                results["recommendations"].append(f"Lower importance_threshold from {config.get('importance_threshold')} to 3 to record more conversations")
            
            if stats.get('memory_count', 0) == 0:
                results["recommendations"].append("No memories recorded yet. Try discussing something important or manually recording a memory")
            
        except Exception as e:
            results["checks"].append({
                "name": "initialize_system",
                "status": "failed",
                "message": f"Failed to initialize: {str(e)}"
            })
            results["issues"].append(f"Initialization error: {str(e)}")
            results["status"] = "unhealthy"
            
    except ImportError as e:
        results["checks"].append({
            "name": "import_modules",
            "status": "failed",
            "message": f"Failed to import modules: {str(e)}"
        })
        results["issues"].append(f"Import error: {str(e)}")
        results["status"] = "unhealthy"
    
    # Check 8: OpenClaw skill status
    try:
        import subprocess
        result = subprocess.run(
            ["openclaw", "skills", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "three-component-memory" in result.stdout:
            results["checks"].append({
                "name": "openclaw_skill",
                "status": "passed",
                "message": "Skill is registered in OpenClaw"
            })
        else:
            results["checks"].append({
                "name": "openclaw_skill",
                "status": "warning",
                "message": "Skill not found in OpenClaw list (may need enabling)"
            })
            results["recommendations"].append("Enable the skill: openclaw config set skills.three-component-memory.enabled true")
    except Exception as e:
        results["checks"].append({
            "name": "openclaw_skill",
            "status": "warning",
            "message": f"Could not check OpenClaw status: {str(e)}"
        })
    
    # Summary
    passed = sum(1 for check in results["checks"] if check["status"] == "passed")
    failed = sum(1 for check in results["checks"] if check["status"] == "failed")
    warning = sum(1 for check in results["checks"] if check["status"] == "warning")
    
    results["summary"] = {
        "total_checks": len(results["checks"]),
        "passed": passed,
        "failed": failed,
        "warning": warning,
        "health_score": int((passed / len(results["checks"])) * 100) if results["checks"] else 0
    }
    
    # Update overall status based on failures
    if failed > 0:
        results["status"] = "unhealthy"
    elif warning > 0:
        results["status"] = "needs_attention"
    
    return results

def print_health_report(results):
    """Print formatted health report."""
    print("=" * 60)
    print("THREE-COMPONENT MEMORY SYSTEM - HEALTH CHECK")
    print("=" * 60)
    
    # Overall status
    status_emoji = {
        "healthy": "✅",
        "needs_attention": "⚠️",
        "unhealthy": "❌"
    }
    emoji = status_emoji.get(results["status"], "❓")
    print(f"\nOverall Status: {emoji} {results['status'].upper()}")
    
    # Summary
    summary = results["summary"]
    print(f"\nChecks: {summary['passed']} passed, {summary['warning']} warnings, {summary['failed']} failed")
    print(f"Health Score: {summary['health_score']}%")
    
    # Detailed checks
    print("\n" + "=" * 60)
    print("DETAILED CHECKS")
    print("=" * 60)
    
    for check in results["checks"]:
        status_icon = {
            "passed": "✅",
            "warning": "⚠️",
            "failed": "❌"
        }.get(check["status"], "❓")
        
        print(f"{status_icon} {check['name']}: {check['message']}")
    
    # Issues
    if results["issues"]:
        print("\n" + "=" * 60)
        print("ISSUES FOUND")
        print("=" * 60)
        for issue in results["issues"]:
            print(f"❌ {issue}")
    
    # Recommendations
    if results["recommendations"]:
        print("\n" + "=" * 60)
        print("RECOMMENDATIONS")
        print("=" * 60)
        for rec in results["recommendations"]:
            print(f"💡 {rec}")
    
    # Quick fixes
    print("\n" + "=" * 60)
    print("QUICK FIXES")
    print("=" * 60)
    print("1. Enable skill: openclaw config set skills.three-component-memory.enabled true")
    print("2. Restart gateway: openclaw gateway restart")
    print("3. Check logs: tail -f /tmp/openclaw/openclaw-*.log")
    print("4. Manual test: python -c \"from three_component_memory import MemorySystem; m=MemorySystem(); print(m.get_stats())\"")
    
    print("\n" + "=" * 60)

def main():
    """Main function."""
    print("Running health checks for Three-Component Memory System...")
    
    try:
        results = check_health()
        print_health_report(results)
        
        # Save results to file
        output_file = Path.home() / ".openclaw" / "memory_health_report.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nFull report saved to: {output_file}")
        
        # Exit code based on status
        if results["status"] == "unhealthy":
            sys.exit(1)
        elif results["status"] == "needs_attention":
            sys.exit(2)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"Error running health check: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()