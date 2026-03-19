# Configuration Guide

Complete guide to configuring the Three-Component Memory System.

## Quick Configuration

### Minimal Setup
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

### Recommended Settings
```json
{
  "skills": {
    "three-component-memory": {
      "enabled": true,
      "auto_record": true,
      "importance_threshold": 3,
      "search_limit": 10,
      "embedding_model": "all-MiniLM-L6-v2",
      "vector_dimension": 384,
      "max_memories": 10000,
      "cleanup_days": 30,
      "debug": false
    }
  }
}
```

## Configuration Options

### Core Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable/disable the entire memory system |
| `auto_record` | boolean | `true` | Automatically record important conversations |
| `importance_threshold` | integer | `3` | Minimum importance score to auto-record (1-5) |

### Search Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `search_limit` | integer | `10` | Maximum number of results per search |
| `search_type` | string | `"hybrid"` | Default search type: "text", "semantic", or "hybrid" |
| `similarity_threshold` | float | `0.7` | Minimum similarity score for semantic search (0.0-1.0) |

### Storage Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `max_memories` | integer | `10000` | Maximum number of memories to store |
| `cleanup_days` | integer | `30` | Auto-delete memories older than this many days |
| `storage_path` | string | `~/.openclaw/memory/three_component/` | Where to store memory data |

### Performance Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `embedding_model` | string | `"all-MiniLM-L6-v2"` | Sentence transformer model for embeddings |
| `vector_dimension` | integer | `384` | Dimension of embedding vectors |
| `batch_size` | integer | `32` | Batch size for embedding generation |
| `cache_embeddings` | boolean | `true` | Cache embeddings for faster search |

### Advanced Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `debug` | boolean | `false` | Enable debug logging |
| `log_level` | string | `"INFO"` | Logging level: DEBUG, INFO, WARNING, ERROR |
| `backup_enabled` | boolean | `true` | Enable automatic backups |
| `backup_interval_hours` | integer | `24` | How often to create backups |

## Importance Scoring

The system automatically scores conversations for importance:

### Scoring Factors
1. **Keywords**: Mentions of "重要", "记住", "决策", "规划", etc.
2. **Length**: Longer, detailed discussions get higher scores
3. **Structure**: Organized content (lists, steps, decisions) scores higher
4. **User Signals**: Explicit requests like "记住这个" boost importance

### Score Ranges
- **1-2**: Casual chat, greetings, simple questions
- **3**: Useful information, explanations, tutorials
- **4**: Important discussions, decisions, plans
- **5**: Critical information, key decisions, must-remember items

## Search Configuration

### Search Types

#### 1. Text Search (`search_type: "text"`)
- **How it works**: Traditional keyword matching
- **Best for**: Finding exact phrases or specific terms
- **Example**: `memory.search("Python decorator", search_type="text")`

#### 2. Semantic Search (`search_type: "semantic"`)
- **How it works**: Vector similarity based on meaning
- **Best for**: Finding conceptually related content
- **Example**: `memory.search("code optimization", search_type="semantic")`

#### 3. Hybrid Search (`search_type: "hybrid"`)
- **How it works**: Combines text and semantic search
- **Best for**: General purpose, balanced results
- **Example**: `memory.search("project planning", search_type="hybrid")`

### Tuning Search Results

```python
# Adjust similarity threshold
memory.config("similarity_threshold", 0.8)  # More strict
memory.config("similarity_threshold", 0.5)  # More lenient

# Change default search type
memory.config("search_type", "semantic")

# Limit results
memory.config("search_limit", 5)  # Fewer results
```

## Storage Management

### Data Locations
```
~/.openclaw/memory/three_component/
├── lancedb/           # Vector embeddings (LanceDB)
│   ├── data.lance     # Embedding data
│   └── schema.json    # Schema definition
├── memory.db          # Structured data (SQLite)
│   ├── memories       # Memory records
│   ├── metadata       # System metadata
│   └── statistics     # Usage stats
├── graph/             # Relationship network (NetworkX)
│   ├── graph.pkl      # Graph structure
│   └── nodes.csv      # Node data
└── backups/           # Automatic backups
    └── 2024-03-19/    # Daily backup folders
```

### Storage Optimization

```python
# Check storage usage
stats = memory.get_stats()
print(f"Memories: {stats['memory_count']}")
print(f"Storage: {stats['storage_size_mb']} MB")

# Clean up old memories
memory.cleanup(days=30)  # Delete memories older than 30 days

# Export memories
memory.export("memories_backup.json")

# Import memories
memory.import("memories_backup.json")
```

## Performance Tuning

### For Large Memory Sets (>5000 memories)
```json
{
  "skills": {
    "three-component-memory": {
      "batch_size": 64,
      "cache_embeddings": true,
      "vector_dimension": 384,
      "max_memories": 50000
    }
  }
}
```

### For Faster Search
```json
{
  "skills": {
    "three-component-memory": {
      "search_limit": 5,
      "similarity_threshold": 0.8,
      "embedding_model": "all-MiniLM-L6-v2"
    }
  }
}
```

### For Lower Memory Usage
```json
{
  "skills": {
    "three-component-memory": {
      "vector_dimension": 128,
      "max_memories": 1000,
      "cache_embeddings": false
    }
  }
}
```

## Environment Variables

You can also configure via environment variables:

```bash
export THREE_COMPONENT_AUTO_RECORD=true
export THREE_COMPONENT_IMPORTANCE_THRESHOLD=3
export THREE_COMPONENT_SEARCH_LIMIT=10
export THREE_COMPONENT_STORAGE_PATH="/custom/path/memory"
```

## Configuration via Python API

```python
from three_component_memory import MemorySystem

memory = MemorySystem()

# Get current configuration
config = memory.get_config()
print(config)

# Update individual settings
memory.config("auto_record", True)
memory.config("importance_threshold", 4)
memory.config("search_limit", 20)

# Update multiple settings
memory.update_config({
    "auto_record": True,
    "importance_threshold": 3,
    "search_type": "hybrid"
})

# Reset to defaults
memory.reset_config()
```

## Troubleshooting Configuration

### Common Issues

1. **Skill not enabled**
   ```bash
   # Check if skill is enabled
   openclaw skills list | grep three-component-memory
   
   # Enable it
   openclaw config set skills.three-component-memory.enabled true
   openclaw gateway restart
   ```

2. **Configuration not taking effect**
   ```bash
   # Check current config
   openclaw config get skills.three-component-memory
   
   # Reload configuration
   openclaw gateway restart
   ```

3. **Storage permissions**
   ```bash
   # Check storage directory permissions
   ls -la ~/.openclaw/memory/three_component/
   
   # Fix permissions if needed
   chmod 755 ~/.openclaw/memory/three_component/
   ```

### Diagnostic Commands

```python
# Run health check
from three_component_memory.utils import check_health
health = check_health()
print(health)

# Check configuration
from three_component_memory import MemorySystem
memory = MemorySystem()
print("Config:", memory.get_config())
print("Stats:", memory.get_stats())
```

## Best Practices

### For Personal Use
- Start with `importance_threshold: 3`
- Enable `auto_record: true`
- Use `search_type: "hybrid"` for balanced results
- Set `cleanup_days: 90` to keep more history

### For Team/Project Use
- Set `importance_threshold: 4` to be more selective
- Increase `max_memories: 50000` for larger teams
- Use `search_type: "semantic"` for better concept matching
- Enable backups with `backup_enabled: true`

### For Development/Debugging
- Set `debug: true` to see detailed logs
- Lower `similarity_threshold: 0.5` to see more results
- Disable `auto_record: false` to control recording manually
- Use smaller `vector_dimension: 128` for faster testing