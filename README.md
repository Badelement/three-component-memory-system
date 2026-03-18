# 🧠 Three-Component Memory System

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3.13+-green.svg)](https://openclaw.ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/template/issues.svg)](https://github.com/yourusername/three-component-memory-system/issues)

## 中文

想看英文版本：[`跳转到 English`](#english)

### 中文简介

用于 OpenClaw 的智能记忆管理系统：将 **LanceDB**（向量检索）、**SQLite**（结构化存储）以及 **NetworkX**（关系图）结合，实现自动对话录入、语义记忆检索，并可减少 **70%-90%** 的 token 使用量。

### 中文功能特点

### 核心功能
- **自动对话录入**：智能记录重要讨论内容
- **语义记忆搜索**：按“含义”而不是关键词查找记忆
- **Token 优化**：将 token 使用量降低 70%-90%
- **本地与私有**：所有数据均保存在本地，无云端依赖

### 技术优势
- **快速性能**：检索响应时间 < 20ms
- **智能关系**：自动发现记忆之间的连接
- **可扩展设计**：随记忆数量线性增长
- **易集成**：提供简单的 OpenClaw skill 接口

### 中文快速安装

### OpenClaw 用户
```bash
# 克隆仓库
git clone https://github.com/yourusername/three-component-memory-system.git

# 运行安装脚本
cd three-component-memory-system
./scripts/setup_env.sh
```

### 手动安装
```bash
# 安装依赖
pip install lancedb networkx sentence-transformers

# 拷贝到 OpenClaw skills 目录
cp -r src ~/.openclaw/skills/three-component-memory

# 配置 OpenClaw（编辑 ~/.openclaw/config.json）
{
  "skills": {
    "three-component-memory": {
      "enabled": true,
      "auto_record": true,
      "importance_threshold": 3
    }
  }
}

# 重启 OpenClaw
openclaw gateway restart
```

### 中文快速开始

### 基本用法
```python
from three_component_memory import MemorySystem

# 初始化系统
memory = MemorySystem()

# 添加一条记忆
memory.add(
    content="Project decision: Use microservices architecture",
    category="project",
    importance=4
)

# 搜索记忆
results = memory.search("project planning", search_type="semantic")
for mem in results:
    print(f"Found: {mem.content[:50]}...")
```

### OpenClaw 命令
```
/memory search <query> [--type semantic|text|hybrid]  # 搜索记忆
/memory stats                                        # 查看系统统计信息
/memory config <key> <value>                       # 更新配置
```

### 中文文档
- **[Getting Started](docs/getting-started.md)** - 完整安装与基础使用指南
- **[API Reference](docs/api-reference.md)** - 详细 API 文档
- **[Architecture](docs/architecture.md)** - 技术架构与设计说明
- **[Examples](examples/)** - 不同使用场景的代码示例

[`跳转到 English`](#english)

## English

A smart memory management system for OpenClaw that combines **LanceDB** (vector search), **SQLite** (structured storage), and **NetworkX** (relationship graph) to provide automatic conversation recording, semantic search, and 70-90% token savings.

想看中文版本：[`跳转到 中文`](#中文)


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
/memory search <query> [--type semantic|text|hybrid]
/memory stats                    # Show system statistics
/memory config <key> <value>     # Update configuration
```

## 📚 Documentation

- **[Getting Started](docs/getting-started.md)** - Complete installation and basic usage guide
- **[API Reference](docs/api-reference.md)** - Detailed API documentation
- **[Architecture](docs/architecture.md)** - Technical architecture and design decisions
- **[Examples](examples/)** - Code examples for various use cases

## 🏗️ Architecture

### Three-Component Design
```
User Conversation → Three-Component System → Intelligent Response
                        ↓
        LanceDB (Semantic) + SQLite (Structured) + NetworkX (Relationships)
```

### Component Details
- **LanceDB**: Vector-based semantic search using all-MiniLM-L6-v2 model
- **SQLite**: Structured metadata storage with full-text search
- **NetworkX**: Relationship graph for discovering memory connections

## 🔧 Development

### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/three-component-memory-system.git
cd three-component-memory-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Project Structure
```
src/                    # Source code
├── __init__.py        # Main entry point
├── memory_core.py     # Core implementation
└── utils/             # Utility modules

docs/                  # Documentation
examples/              # Usage examples
tests/                 # Test suite
scripts/               # Utility scripts
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 🐛 Reporting Issues

Found a bug or have a feature request? Please [open an issue](https://github.com/yourusername/three-component-memory-system/issues).

When reporting issues, please include:
- Steps to reproduce
- Expected vs actual behavior
- System information (Python version, OpenClaw version, etc.)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenClaw Team** for the amazing AI assistant platform
- **LanceDB** for the excellent vector database
- **NetworkX** for the powerful graph library
- **Sentence Transformers** for the embedding models

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/three-component-memory-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/three-component-memory-system/discussions)

---

**Project Status**: Active Development  
**Version**: 1.1.0  
**Last Updated**: 2026-03-18
