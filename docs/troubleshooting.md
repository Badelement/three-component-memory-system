# Troubleshooting Guide

## Quick Diagnosis

### System Status Check
```bash
# Run the diagnostic script
python scripts/diagnose.py

# Or check manually
python -c "
import sys
sys.path.insert(0, 'src')
from three_component_memory import MemorySystem
try:
    memory = MemorySystem()
    stats = memory.get_stats()
    print('✅ System Status:', stats.get('status', 'unknown'))
    print('✅ Memory Count:', stats.get('memory_count', 0))
except Exception as e:
    print('❌ Error:', e)
"
```

## Common Issues

### Installation Issues

#### Issue: ImportError when importing
```
ModuleNotFoundError: No module named 'three_component_memory'
```

**Causes:**
1. Skill directory not in Python path
2. Missing __init__.py file
3. Incorrect module name

**Solutions:**
1. Check skill directory exists:
   ```bash
   ls -la ~/.openclaw/skills/three-component-memory/
   ```

2. Verify Python path includes the directory:
   ```python
   import sys
   sys.path.insert(0, "/Users/yourusername/.openclaw/skills/three-component-memory")
   from __init__ import MemorySystem
   ```

3. Check for __init__.py:
   ```bash
   ls -la ~/.openclaw/skills/three-component-memory/__init__.py
   ```

#### Issue: Missing dependencies
```
ImportError: No module named 'lancedb'
```

**Solution:**
```bash
# Install all dependencies
pip install lancedb networkx sentence-transformers numpy

# Or install from requirements
pip install -r requirements.txt
```

### Configuration Issues

#### Issue: Auto-record not working
**Symptoms:**
- Important conversations not being recorded
- No new memories appearing in searches

**Diagnosis:**
1. Check configuration:
   ```bash
   cat ~/.openclaw/config.json | python -m json.tool | grep -A10 "three-component-memory"
   ```

2. Verify settings:
   - `enabled` should be `true`
   - `auto_record` should be `true`
   - `importance_threshold` should be ≤ 3 (default)

**Solutions:**
1. Update configuration:
   ```json
   {
     "skills": {
       "three-component-memory": {
         "enabled": true,
         "auto_record": true,
         "importance_threshold": 3
       }
     }
   }
   ```

2. Restart OpenClaw:
   ```bash
   openclaw gateway restart
   ```

#### Issue: Search returning no results
**Symptoms:**
- Searches return empty results
- Even with known existing memories

**Diagnosis:**
1. Check memory count:
   ```python
   stats = memory.get_stats()
   print(f"Memory count: {stats.get('memory_count', 0)}")
   ```

2. Test different search types:
   ```python
   # Test all search types
   for search_type in ["semantic", "text", "hybrid"]:
       results = memory.search("test", search_type=search_type)
       print(f"{search_type}: {len(results)} results")
   ```

**Solutions:**
1. Ensure there are memories in the system
2. Try different search types
3. Adjust search parameters:
   ```python
   # Lower minimum score
   results = memory.search("query", min_score=0.1)
   
   # Increase limit
   results = memory.search("query", limit=20)
   ```

### Performance Issues

#### Issue: Slow search performance
**Symptoms:**
- Searches taking >100ms
- System feels sluggish

**Diagnosis:**
1. Check memory count:
   ```python
   stats = memory.get_stats()
   count = stats.get('memory_count', 0)
   print(f"Total memories: {count}")
   ```

2. Profile performance:
   ```bash
   python scripts/benchmark.py
   ```

**Solutions:**
1. For large datasets (>10,000 memories):
   ```python
   # Enable caching
   memory = MemorySystem({"cache_enabled": True, "cache_size": 1000})
   ```

2. Optimize queries:
   ```python
   # Use more specific queries
   results = memory.search("specific topic", limit=5)
   
   # Avoid overly broad searches
   # ❌ Bad: memory.search("project")
   # ✅ Good: memory.search("project timeline Q4 2026")
   ```

3. Clean up old memories:
   ```python
   # Export and archive old memories
   memory.export("old_memories.json")
   ```

#### Issue: High memory usage
**Symptoms:**
- System using >500MB RAM
- Slow performance on low-memory devices

**Solutions:**
1. Reduce cache size:
   ```python
   memory = MemorySystem({"cache_size": 100})  # Default is 1000
   ```

2. Limit memory count:
   ```python
   # Implement automatic cleanup
   if memory.get_stats()["memory_count"] > 10000:
       print("Consider archiving old memories")
   ```

3. Use lighter models:
   ```python
   # If using custom embedding model
   memory = MemorySystem({"embedding_model": "all-MiniLM-L6-v2"})  # Lightweight
   ```

### Data Issues

#### Issue: LanceDB directory empty
**Symptoms:**
- `~/.openclaw/memory/three_component/lancedb/` directory is empty
- Semantic search may not work properly

**Solutions:**
1. Check permissions:
   ```bash
   ls -la ~/.openclaw/memory/three_component/
   chmod 755 ~/.openclaw/memory/three_component/lancedb/
   ```

2. Reinitialize LanceDB:
   ```python
   # This should happen automatically on first use
   # Try adding a memory
   memory_id = memory.add("Test memory for initialization")
   ```

3. Check LanceDB logs:
   ```python
   memory = MemorySystem({"debug": True})
   # Check console output for LanceDB errors
   ```

#### Issue: SQLite database errors
**Symptoms:**
- Database corruption errors
- "database is locked" errors
- Data inconsistency

**Solutions:**
1. Backup and repair:
   ```bash
   # Backup database
   cp ~/.openclaw/memory/three_component/memory.db ~/backup/memory.db.backup
   
   # Try SQLite repair
   sqlite3 ~/.openclaw/memory/three_component/memory.db "VACUUM;"
   ```

2. Check for locks:
   ```bash
   # Check if another process has the database open
   lsof ~/.openclaw/memory/three_component/memory.db 2>/dev/null || echo "No locks found"
   ```

3. Recreate database (last resort):
   ```python
   # Export all data
   data = memory.export("backup.json")
   
   # Delete and recreate
   import os
   os.remove("~/.openclaw/memory/three_component/memory.db")
   
   # Recreate memory system
   memory = MemorySystem()
   
   # Import data
   memory.import("backup.json")
   ```

## Advanced Troubleshooting

### Debug Mode
Enable debug mode for detailed logging:
```python
memory = MemorySystem({"debug": True})

# All operations will log details
memory.search("test")
```

Debug output includes:
- Component initialization status
- Query execution times
- Error details and stack traces
- Memory usage statistics

### System Health Check
Run comprehensive health check:
```python
def health_check(memory):
    import os
    
    stats = memory.get_stats()
    
    checks = {
        "database": os.path.exists(os.path.expanduser("~/.openclaw/memory/three_component/memory.db")),
        "lancedb": os.path.exists(os.path.expanduser("~/.openclaw/memory/three_component/lancedb/")),
        "graph": os.path.exists(os.path.expanduser("~/.openclaw/memory/three_component/graph/")),
        "config": stats.get("config_loaded", False),
        "memory_count": stats.get("memory_count", 0) > 0,
        "components_healthy": all(stats.get("component_status", {}).values())
    }
    
    return {
        "healthy": all(checks.values()),
        "checks": checks,
        "stats": stats
    }

result = health_check(memory)
print(f"System healthy: {result['healthy']}")
for check, status in result['checks'].items():
    print(f"  {check}: {'✅' if status else '❌'}")
```

### Performance Profiling
Profile system performance:
```python
import cProfile
import pstats

def profile_search():
    memory = MemorySystem()
    
    def test_searches():
        for i in range(100):
            memory.search(f"test query {i}")
    
    cProfile.runctx('test_searches()', globals(), locals(), 'profile_stats')
    
    stats = pstats.Stats('profile_stats')
    stats.sort_stats('time').print_stats(10)

profile_search()
```

## Recovery Procedures

### Complete System Reset
If all else fails, reset the system:

1. **Backup data:**
   ```bash
   mkdir -p ~/backup/openclaw-memory
   cp -r ~/.openclaw/memory/three_component ~/backup/openclaw-memory/
   cp ~/.openclaw/config.json ~/backup/openclaw-memory/
   ```

2. **Remove old data:**
   ```bash
   rm -rf ~/.openclaw/memory/three_component
   ```

3. **Reinstall skill:**
   ```bash
   # Re-copy skill files
   cp -r /path/to/skill ~/.openclaw/skills/three-component-memory
   ```

4. **Reconfigure:**
   ```bash
   # Ensure config.json has correct settings
   ```

5. **Restart:**
   ```bash
   openclaw gateway restart
   ```

### Data Migration
Migrate to new version or system:

1. **Export all data:**
   ```python
   data = memory.export("full_export.json")
   ```

2. **Convert format if needed**
3. **Import to new system**

## Getting Help

### Collect Diagnostic Information
Before asking for help, collect:
```python
import sys
import platform
import json

diagnostics = {
    "version": "1.1.0",
    "config": memory.get_config(),
    "stats": memory.get_stats(),
    "system": {
        "python": sys.version,
        "platform": platform.platform(),
        "openclaw_config": "~/.openclaw/config.json"
    },
    "error": "Describe the error here"
}

print(json.dumps(diagnostics, indent=2))
```

### Contact Support
Include in your request:
1. Error messages and stack traces
2. Diagnostic information
3. Steps to reproduce the issue
4. What you've tried already

### Community Support
- **GitHub Issues**: [Open an issue](https://github.com/yourusername/three-component-memory-system/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/yourusername/three-component-memory-system/discussions)
- **OpenClaw Discord**: Join the OpenClaw community

---

**Troubleshooting Guide Version**: 1.0.0  
**Last Updated**: 2026-03-18
