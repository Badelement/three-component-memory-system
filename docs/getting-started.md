# Getting Started

This guide will help you install and start using the Three-Component Memory System.

## Prerequisites

- **Python 3.8 or higher**
- **OpenClaw** installed and running
- **Git** (for cloning the repository)

## Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/three-component-memory-system.git
cd three-component-memory-system

# Run the setup script
./scripts/setup_env.sh
```

The setup script will:
1. Check system requirements
2. Install Python dependencies
3. Configure OpenClaw
4. Test the installation

### Method 2: Manual Installation

#### Step 1: Install Dependencies
```bash
pip install lancedb networkx sentence-transformers numpy
```

#### Step 2: Install the Skill
```bash
# Clone or download the repository
git clone https://github.com/yourusername/three-component-memory-system.git

# Copy to OpenClaw skills directory
mkdir -p ~/.openclaw/skills/
cp -r three-component-memory-system/src ~/.openclaw/skills/three-component-memory
```

#### Step 3: Configure OpenClaw

Edit `~/.openclaw/config.json` and add:

```json
{
  "skills": {
    "three-component-memory": {
      "enabled": true,
      "auto_record": true,
      "importance_threshold": 3,
      "data_path": "~/.openclaw/memory/three_component"
    }
  }
}
```

#### Step 4: Restart OpenClaw
```bash
openclaw gateway restart
```

## Basic Usage

### Python API

```python
from three_component_memory import MemorySystem

# Initialize the system
memory = MemorySystem()

# Add a memory
memory_id = memory.add(
    content="Important project decision",
    category="project",
    tags=["decision", "important"],
    importance=4
)

# Search memories
results = memory.search("project planning", search_type="semantic")
for mem in results:
    print(f"Score: {mem.score:.3f} - {mem.content[:50]}...")

# Get system statistics
stats = memory.get_stats()
print(f"Total memories: {stats['memory_count']}")
```

### OpenClaw Commands

Once installed, you can use these commands in OpenClaw:

```
/memory search <query> [--type semantic|text|hybrid] [--limit 5]
/memory stats                    # Show system statistics
/memory config <key> <value>     # Update configuration
```

### Example: Recording a Conversation

The system automatically records important conversations. You can also manually add memories:

```python
# Record an important conversation
memory.auto_record(
    user_message="How does the three-component system work?",
    ai_response="It combines LanceDB for semantic search, SQLite for structured storage, and NetworkX for relationship graphs."
)
```

## Configuration

### Default Configuration

```yaml
enabled: true
auto_record: true
importance_threshold: 3
data_path: ~/.openclaw/memory/three_component
search:
  default_type: hybrid
  default_limit: 5
  min_score: 0.3
```

### Customizing Configuration

Edit `~/.openclaw/config.json`:

```json
{
  "skills": {
    "three-component-memory": {
      "enabled": true,
      "auto_record": true,
      "importance_threshold": 4,
      "data_path": "~/custom/path/to/memories",
      "search": {
        "default_type": "semantic",
        "default_limit": 10,
        "min_score": 0.2
      }
    }
  }
}
```

## Testing the Installation

Run the test script to verify everythingis working:

```bash
# Run the test script
python scripts/test_installation.py
```

Or test manually:

```python
import sys
sys.path.insert(0, "src")
from three_component_memory import MemorySystem

memory = MemorySystem()
print("✅ System initialized successfully")

stats = memory.get_stats()
print(f"✅ System status: {stats['status']}")
```

## Troubleshooting

### Common Issues

#### Issue: ImportError
```
ModuleNotFoundError: No module named 'three_component_memory'
```

**Solution**: Ensure the skill is in the correct directory:
```bash
ls -la ~/.openclaw/skills/three-component-memory/
```

#### Issue: Dependencies Missing
```
ImportError: No module named 'lancedb'
```

**Solution**: Install dependencies:
```bash
pip install lancedb networkx sentence-transformers
```

#### Issue: Auto-record Not Working
**Solution**: Check configuration:
```bash
cat ~/.openclaw/config.json | grep -A5 "three-component-memory"
```

Ensure `auto_record` is `true` and `importance_threshold` is appropriate.

## Next Steps

Now that you have the system installed, you can:

1. **Try the examples**: Check out the [examples directory](../examples/)
2. **Read the API documentation**: See [API Reference](api-reference.md)
3. **Learn about the architecture**: Read [Architecture](architecture.md)
4. **Start using it**: The system will automatically record important conversations

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](../docs/troubleshooting.md)
2. Search [GitHub Issues](https://github.com/yourusername/three-component-memory-system/issues)
3. Ask in [GitHub Discussions](https://github.com/yourusername/three-component-memory-system/discussions)
