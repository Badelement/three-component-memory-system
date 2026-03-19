---
name: three-component-memory
description: |
  Smart memory management system that automatically records important conversations, enables semantic search, and saves 70-90% tokens. 
  
  **ALWAYS use this skill when the user:**
  - Mentions remembering, recording, or saving important discussions
  - Asks about reducing token usage or optimizing conversation history
  - Wants to search for past conversations by meaning (not just keywords)
  - Needs a local, privacy-first memory system for AI conversations
  - Talks about "三组件", "记忆系统", "token优化", or "上下文管理"
  
  **Even if they don't explicitly ask for "memory system", use this skill when they:**
  - Say "记住这个" or "这个很重要"
  - Complain about long conversation history or high token usage
  - Want to find something discussed before but can't remember exact words
  - Need to build a personal knowledge base from conversations
---

# Three-Component Memory System

A smart memory system that automatically records what matters, finds memories by meaning, and cuts token usage by 70-90%.

## 🚀 Get Started in 30 Seconds

### 1. Check if it's enabled
```bash
openclaw skills list | grep three-component-memory
```

### 2. Use it right now
The system works automatically. Important conversations are already being recorded.

**Search your memories:**
```python
from three_component_memory import MemorySystem
memory = MemorySystem()
results = memory.search("your search query")
```

**Or use OpenClaw commands:**
```
/memory search <query>     # Find memories by meaning
/memory stats              # See what's been recorded
/memory config auto_record true  # Turn on automatic recording
```

## 🎯 What This Skill Does

### Automatically Records What Matters
- **Listens** to conversations in real-time
- **Identifies** important discussions (not casual chat)
- **Saves** key information with semantic understanding
- **Ignores** routine messages and system chatter

### Finds Memories by Meaning (Not Keywords)
```python
# Searches understand what you mean
memory.search("project planning")  # Finds: "项目规划", "sprint planning", "roadmap discussion"
memory.search("code optimization") # Finds: "性能优化", "算法改进", "效率提升"
```

### Cuts Token Usage Dramatically
- **Before**: Full conversation history (1000+ tokens)
- **After**: Only relevant memories (100-300 tokens)
- **Savings**: 70-90% reduction in context length

## 📖 Learn More When You Need It

The detailed documentation is in `references/` - read it when you need specific information:

- **[API Reference](references/API_REFERENCE.md)** - Complete Python API with examples
- **[Configuration Guide](references/CONFIGURATION.md)** - All settings and tuning options
- **[Troubleshooting](references/TROUBLESHOOTING.md)** - Fix common issues
- **[Architecture](references/ARCHITECTURE.md)** - How the three components work together

## 🔧 Common Tasks

### Record an Important Discussion
```python
# The system automatically detects importance
# But you can explicitly mark something:
memory.record("Project decision: We'll use FastAPI for the backend", importance=5)
```

### Search Your Memory Bank
```python
# Different search types for different needs
results = memory.search("resource allocation", search_type="hybrid")  # Best match (default)
results = memory.search("exact phrase here", search_type="text")     # Text match only
results = memory.search("similar concepts", search_type="semantic")  # Meaning match only
```

### Optimize Existing Conversations
```python
# Reduce token usage for long histories
optimized = memory.optimize_context(full_conversation_history)
# Returns only the relevant memories (70-90% smaller)
```

## ⚙️ Minimal Configuration

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

## 🚨 When Things Go Wrong

### Quick Fixes
1. **Skill not triggering?** Check it's enabled: `openclaw skills list`
2. **No memories found?** Lower the importance threshold
3. **Search too slow?** Check `memory.get_stats()` for index health
4. **Storage full?** Data is at `~/.openclaw/memory/three_component/`

### Get Help
Run the diagnostic script:
```bash
python scripts/check_health.py
```

---

**Key Principle**: This system works best when you forget it's there. It quietly records what matters, so you can focus on the conversation, not on managing memory.

**Pro Tip**: The more you use it, the better it gets at understanding what's important to you.