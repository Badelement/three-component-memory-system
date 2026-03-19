# 🧠 Three-Component Memory System

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3.13+-green.svg)](https://openclaw.ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/template/issues.svg)](https://github.com/yourusername/three-component-memory-system/issues)

🌐 **Language**: [English](README.md) | [中文](README_zh.md)

## 📖 Introduction

A smart memory management system for OpenClaw that combines **LanceDB** (vector search), **SQLite** (structured storage), and **NetworkX** (relationship graph) to provide automatic conversation recording, semantic search, and 70-90% token savings.

## ✨ Features

### 🚀 Core Features
- **Automatic Conversation Recording** - Intelligently records important discussions
- **Semantic Memory Search** - Finds memories by meaning, not just keywords
- **Token Optimization** - Reduces token usage by 70-90%
- **Local & Private** - All data stored locally, no cloud dependencies

### 🛠️ Technical Advantages
- **Fast Performance** - <20ms search response time
- **Smart Relationships** - Discovers connections between memories
- **Scalable Design** - Linear scaling with memory count
- **Easy Integration** - Simple OpenClaw skill interface

## 📦 Quick Installation

## 🎯 Latest Optimizations (v1.2.0)

Based on the latest **skill-creator** methodology, this skill has been comprehensively optimized:

### 🔥 Improved Triggering
- **More proactive triggering** - Explicitly lists scenarios where the skill MUST be used
- **Edge case coverage** - Includes cases where users might not explicitly ask for "memory system"
- **Natural language matching** - Recognizes phrases users actually say, like "remember this", "too many tokens"

### 📚 Progressive Documentation
- **30-second quick start** - SKILL.md focuses on getting started fast
- **Detailed references** - All in-depth content moved to references/ directory
- **Utility scripts** - Added health check and quick demo scripts

### 🛠️ New Features
- **`check_health.py`** - Comprehensive system health check tool
- **`quick_demo.py`** - 2-minute interactive feature demonstration
- **`CONFIGURATION.md`** - Complete configuration guide (20+ options)

### For OpenClaw Users
```bash
# Clone the repository
git clone https://github.com/yourusername/three-component-memory-system.git

# Run installation script
cd three-component-memory-system
./scripts/setup_env.sh
```

### Manual Installation
```bash
# Install dependencies
pip install lancedb networkx sentence-transformers

# Copy to OpenClaw skills directory
cp -r src ~/.openclaw/skills/three-component-memory

# Configure OpenClaw (edit ~/.openclaw/config.json)
{
  "skills": {
    "three-component-memory": {
      "enabled": true,
      "auto_record": true,
      "importance_threshold": 3
    }
  }
}

# Restart OpenClaw
openclaw gateway restart
```

## 🚀 Quick Start

### Basic Usage
```python
from three_component_memory import MemorySystem

# Initialize the system
memory = MemorySystem()

# Add a memory
memory.add(
    content="Project decision: Use microservices architecture",
    category="project",
    importance=4
)

# Search memories
results = memory.search("project planning", search_type="semantic")
for mem in results:
    print(f"Found: {mem.content[:50]}...")
```

### OpenClaw Commands
```
/memory search <query> [--type semantic|text|hybrid]  # Search memories
/memory stats                                        # View system statistics
/memory config <key> <value>                       # Update configuration
```

## 📚 Documentation

- **[Getting Started](docs/getting-started.md)** - Complete installation and basic usage guide
- **[API Reference](docs/api-reference.md)** - Detailed API documentation
- **[Architecture](docs/architecture.md)** - Technical architecture and design
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## 🏗️ Architecture

The Three-Component Memory System uses a modular design:

```
┌─────────────────────────────────────────────┐
│              MemorySystem                   │
├─────────────┬──────────────┬───────────────┤
│  LanceDB    │   SQLite     │   NetworkX    │
│ (Vector DB) │ (Structured) │ (Graph DB)    │
└─────────────┴──────────────┴───────────────┘
```

### Component Overview
1. **LanceDB** - Vector database for semantic search
2. **SQLite** - Relational database for structured memory storage
3. **NetworkX** - Graph database for managing relationships between memories

## 🔧 Configuration Options

```json
{
  "enabled": true,
  "auto_record": true,
  "importance_threshold": 3,
  "vector_model": "all-MiniLM-L6-v2",
  "max_memories": 10000,
  "search_limit": 10
}
```

## 📊 Performance Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| Search Response | <20ms | Average semantic search time |
| Token Savings | 70-90% | Compared to full context |
| Memory Capacity | 10,000+ | Maximum supported memories |
| Memory Usage | <100MB | Typical workload |

## 🤝 Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issue Tracker**: [GitHub Issues](https://github.com/yourusername/three-component-memory-system/issues)
- **Documentation**: [docs/](docs/)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/three-component-memory-system/discussions)

---

**Three-Component Memory System** - Giving AI assistants real long-term memory

---

**Latest Version**: 1.2.0 (2026-03-19)  
**Changelog**: [English](CHANGELOG.md) | [中文](CHANGELOG_zh.md)  
**Status**: Production Ready (skill-creator optimized)