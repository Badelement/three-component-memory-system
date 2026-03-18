---
name: three-component-memory
description: Smart memory management system combining LanceDB (vector search), SQLite (structured storage), and NetworkX (relationship graph). Provides automatic conversation recording, semantic search, and 70-90% token savings. Use when: (1) Managing conversation history intelligently, (2) Reducing token usage in AI conversations, (3) Implementing semantic search for memories, (4) Building local, privacy-first memory systems.
---

# Three-Component Memory System

A smart memory management system that automatically records important conversations, enables semantic search, and saves 70-90% tokens through structured storage.

## 🚀 Quick Start

### Installation (Already Installed)
The skill is pre-installed in OpenClaw. Just enable it:

```bash
# Check if skill is available
openclaw skills list | grep three-component-memory

# Enable if needed
openclaw config set skills.three-component-memory.enabled true
openclaw gateway restart
```

### First Use
```python
from three_component_memory import MemorySystem

# System auto-initializes and starts recording
memory = MemorySystem()

# Search your memories
results = memory.search("project planning")
```

### OpenClaw Commands
```
/memory search <query>           # Search memories (hybrid by default)
/memory stats                    # Show memory statistics
/memory config <key> <value>     # Update configuration
```

## 🎯 When to Use This Skill

### Primary Use Cases
1. **Intelligent conversation history** - Automatically records important discussions
2. **Token optimization** - Reduces context token usage by 70-90%
3. **Semantic search** - Finds memories by meaning, not just keywords
4. **Local memory system** - Privacy-first, no cloud dependencies

### Trigger Keywords
- "记住这个" / "记住" / "重要"
- "搜索记忆" / "查找之前的讨论"
- "token太多" / "上下文太长"
- "三组件" / "记忆系统"

## ⚙️ Configuration

### Minimal Configuration
Add to `~/.openclaw/config.json`:
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

### Common Settings
```yaml
auto_record: true          # Auto-record important conversations
importance_threshold: 3    # 1-5, higher = more selective
search_limit: 5           # Default results per search
debug: false              # Enable debug logging
```

## 🔧 Core Workflows

### 1. Automatic Recording
- **Records**: Conversations with importance ≥ 3
- **Ignores**: Casual chatter, system messages
- **Keywords**: "重要", "决策", "记住", "token", "三组件"

### 2. Semantic Search
```python
# Find related memories by meaning
memory.search("resource optimization")

# Different search types
memory.search("exact phrase", search_type="text")
memory.search("similar concept", search_type="semantic")
memory.search("best match", search_type="hybrid")  # default
```

### 3. Context Optimization
- **Before**: Full conversation history (1000+ tokens)
- **After**: Only relevant memories (100-300 tokens)
- **Savings**: 70-90% token reduction

## 📚 Detailed Documentation

For complete information, see the references directory:

- **[ARCHITECTURE.md](references/ARCHITECTURE.md)** - Technical design and components
- **[API_REFERENCE.md](references/API_REFERENCE.md)** - Complete Python API
- **[EXAMPLES.md](references/EXAMPLES.md)** - Usage patterns and examples
- **[TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** - Problem-solving guide

## 🛠️ Maintenance

### Data Location
```
~/.openclaw/memory/three_component/
├── lancedb/     # Vector embeddings
├── memory.db    # Structured data (SQLite)
└── graph/       # Relationship network
```

### Quick Checks
```bash
# Check skill status
openclaw skills info three-component-memory

# Check memory count
python -c "from three_component_memory import MemorySystem; m=MemorySystem(); print(m.get_stats())"
```

## ⚡ Performance

- **Search speed**: <20ms per query
- **Memory capacity**: 10,000+ memories
- **Token savings**: 70-90% reduction
- **Storage**: ~100MB for 10,000 memories

## 🔄 Updates

The skill auto-updates with OpenClaw. Check for updates:
```bash
openclaw skills sync
```

---

**Version**: 1.1.0  
**Status**: Production Ready  
**Last Verified**: 2026-03-19