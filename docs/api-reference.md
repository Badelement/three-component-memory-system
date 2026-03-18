# API Reference

## MemorySystem Class

### Constructor
```python
MemorySystem(config=None)
```

Initialize the memory system.

**Parameters:**
- `config` (dict, optional): Configuration dictionary
  - `auto_record` (bool): Enable automatic recording (default: True)
  - `importance_threshold` (int): Minimum importance to record (1-5, default: 3)
  - `data_path` (str): Data directory path
  - `debug` (bool): Enable debug logging (default: False)

**Example:**
```python
from three_component_memory import MemorySystem

# Default configuration
memory = MemorySystem()

# Custom configuration
memory = MemorySystem({
    "auto_record": True,
    "importance_threshold": 4,
    "data_path": "~/custom/path",
    "debug": True
})
```

## Core Methods

### add()
```python
add(content, category="general", tags=None, importance=3, metadata=None)
```

Add a new memory to the system.

**Parameters:**
- `content` (str): Memory content text
- `category` (str): Category name (default: "general")
- `tags` (list): List of tag strings (default: [])
- `importance` (int): Importance level 1-5 (default: 3)
- `metadata` (dict): Additional metadata (default: {})

**Returns:**
- `str`: Memory ID if successful, `None` if failed

**Example:**
```python
memory_id = memory.add(
    content="Project decision: Use microservices architecture",
    category="project",
    tags=["architecture", "decision", "important"],
    importance=4,
    metadata={"project": "api-gateway", "meeting_date": "2026-03-18"}
)
```

### search()
```python
search(query, search_type="hybrid", limit=5, min_score=0.3)
```

Search memories across three components.

**Parameters:**
- `query` (str): Search query text
- `search_type` (str): "semantic", "text", or "hybrid" (default: "hybrid")
- `limit` (int): Maximum results to return (default: 5)
- `min_score` (float): Minimum relevance score 0.0-1.0 (default: 0.3)

**Returns:**
- `list`: List of Memory objects with scores

**Example:**
```python
# Semantic search
results = memory.search("resource optimization", search_type="semantic")

# Text search
results = memory.search("三组件系统", search_type="text")

# Hybrid search with custom limit
results = memory.search("project planning", search_type="hybrid", limit=10)
```

### get_context()
```python
get_context(current_topic, limit=3)
```

Get relevant context for current conversation topic.

**Parameters:**
- `current_topic` (str): Current conversation topic
- `limit` (int): Maximum context memories to return (default: 3)

**Returns:**
- `list`: List of context dictionaries

**Example:**
```python
context = memory.get_context("discussing API design patterns", limit=3)
for item in context:
    print(f"Relevance: {item['relevance']:.2f}")
    print(f"Content: {item['content'][:100]}...")
```

### get_stats()
```python
get_stats()
```

Get system statistics and status.

**Returns:**
- `dict`: Statistics dictionary

**Example:**
```python
stats = memory.get_stats()
print(f"Status: {stats['status']}")
print(f"Memory count: {stats['memory_count']}")
print(f"Components: {', '.join(stats['components'])}")
```

## Advanced Methods

### auto_record()
```python
auto_record(user_message, ai_response)
```

Automatically record a conversation if important.

**Parameters:**
- `user_message` (str): User message text
- `ai_response` (str): AI response text

**Returns:**
- `str`: Memory ID if recorded, `None` if not recorded

**Example:**
```python
memory_id = memory.auto_record(
    user_message="How does the three-component system work?",
    ai_response="It combines LanceDB, SQLite, and NetworkX..."
)
```

### export()
```python
export(format="json", file_path=None)
```

Export memories to file.

**Parameters:**
- `format` (str): "json", "csv", or "markdown" (default: "json")
- `file_path` (str): Output file path (optional)

**Returns:**
- `str/dict`: Export data or file path

**Example:**
```python
# Export to JSON file
export_path = memory.export(format="json", file_path="memories.json")

# Export to dictionary
data = memory.export(format="json")
```

### import()
```python
import(file_path, merge=True)
```

Import memories from file.

**Parameters:**
- `file_path` (str): Input file path
- `merge` (bool): Merge with existing memories (default: True)

**Returns:**
- `int`: Number of memories imported

**Example:**
```python
count = memory.import("backup/memories.json")
print(f"Imported {count} memories")
```

### cleanup()
```python
cleanup()
```

Perform maintenance operations.

**Example:**
```python
memory.cleanup()  # Optimizes databases, removes temp files
```

## Configuration Methods

### get_config()
```python
get_config()
```

Get current configuration.

**Returns:**
- `dict`: Current configuration

### update_config()
```python
update_config(new_config)
```

Update configuration.

**Parameters:**
- `new_config` (dict): New configuration values

**Example:**
```python
memory.update_config({
    "importance_threshold": 4,
    "auto_record": False
})
```

## Memory Object

### Attributes
```python
class Memory:
    id: str           # Unique memory ID
    content: str      # Memory content text
    category: str     # Category name
    tags: List[str]   # List of tags
    importance: int   # Importance level 1-5
    metadata: dict    # Additional metadata
    created_at: str   # ISO format timestamp
    score: float      # Search relevance score (0.0-1.0)
```

### Example Usage
```python
# Accessing memory attributes
for memory in results:
    print(f"ID: {memory.id}")
    print(f"Content: {memory.content}")
    print(f"Category: {memory.category}")
    print(f"Tags: {', '.join(memory.tags)}")
    print(f"Importance: {memory.importance}/5")
    print(f"Score: {memory.score:.3f}")
```

## Error Handling

### Common Exceptions
```python
try:
    result = memory.search("query")
except MemorySystemError as e:
    print(f"System error: {e}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except DatabaseError as e:
    print(f"Database error: {e}")
```

### Error Recovery
```python
# Check system status
stats = memory.get_stats()
if stats["status"] != "healthy":
    print("System needs maintenance")
    
# Try recovery
memory.cleanup()
```

## Performance Tips

### Batch Operations
```python
# Batch add memories
memory_ids = []
for content in memory_list:
    memory_id = memory.add(content)
    memory_ids.append(memory_id)
```

### Search Optimization
```python
# Use appropriate search type
# - semantic: For meaning-based queries
# - text: For exact keyword matches  
# - hybrid: For general use

# Adjust limit based on needs
results = memory.search("query", limit=20)  # More results
results = memory.search("query", limit=3)   # Fewer, faster
```

## Event Hooks

### Custom Hooks
```python
# Pre-record hook
memory.add_pre_record_hook(lambda msg: print(f"Recording: {msg}"))

# Post-record hook  
memory.add_post_record_hook(lambda mem_id: print(f"Recorded: {mem_id}"))

# Search hook
memory.add_search_hook(lambda query, results: print(f"Search: {query} -> {len(results)} results"))
```

---

**API Version**: 1.1.0  
**Last Updated**: 2026-03-18
