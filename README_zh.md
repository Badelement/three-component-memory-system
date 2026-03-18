# 🧠 三组件记忆系统

[![Python 版本](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw 兼容](https://img.shields.io/badge/OpenClaw-2026.3.13+-green.svg)](https://openclaw.ai)
[![许可证](https://img.shields.io/badge/许可证-MIT-blue.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/bithub/issues/template/issues.svg)](https://github.com/yourusername/three-component-memory-system/issues)

🌐 **语言**: [English](README.md) | [中文](README_zh.md)

## 📖 简介

用于 OpenClaw 的智能记忆管理系统：将 **LanceDB**（向量检索）、**SQLite**（结构化存储）以及 **NetworkX**（关系图）结合，实现自动对话录入、语义记忆检索，并可减少 **70%-90%** 的 token 使用量。

## ✨ 功能特点

### 🚀 核心功能
- **自动对话录入** - 智能记录重要讨论内容
- **语义记忆搜索** - 按"含义"而不是关键词查找记忆
- **Token 优化** - 将 token 使用量降低 70%-90%
- **本地与私有** - 所有数据均保存在本地，无云端依赖

### 🛠️ 技术优势
- **快速性能** - <20ms 搜索响应时间
- **智能关系** - 自动发现记忆之间的连接
- **可扩展设计** - 随记忆数量线性增长
- **易集成** - 提供简单的 OpenClaw skill 接口

## 📦 快速安装

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

## 🚀 快速开始

### 基本用法
```python
from three_component_memory import MemorySystem

# 初始化系统
memory = MemorySystem()

# 添加一条记忆
memory.add(
    content="项目决策：使用微服务架构",
    category="项目",
    importance=4
)

# 搜索记忆
results = memory.search("项目规划", search_type="semantic")
for mem in results:
    print(f"找到：{mem.content[:50]}...")
```

### OpenClaw 命令
```
/memory search <查询> [--type semantic|text|hybrid]  # 搜索记忆
/memory stats                                        # 查看系统统计信息
/memory config <键> <值>                           # 更新配置
```

## 📚 文档

- **[快速开始](docs/zh/getting-started_zh.md)** - 完整安装与基础使用指南
- **[API 参考](docs/zh/api-reference_zh.md)** - 详细 API 文档
- **[架构设计](docs/zh/architecture_zh.md)** - 技术架构与设计说明
- **[故障排除](docs/zh/troubleshooting_zh.md)** - 常见问题与解决方案

所有文档均有中文版本，位于 `docs/zh/` 目录下。

## 🏗️ 架构

三组件记忆系统采用模块化设计：

```
┌─────────────────────────────────────────────┐
│              MemorySystem                   │
├─────────────┬──────────────┬───────────────┤
│  LanceDB    │   SQLite     │   NetworkX    │
│  (向量检索) │ (结构化存储) │  (关系图)     │
└─────────────┴──────────────┴───────────────┘
```

### 组件说明
1. **LanceDB** - 向量数据库，用于语义搜索
2. **SQLite** - 关系数据库，存储结构化记忆数据
3. **NetworkX** - 图数据库，管理记忆之间的关系

## 🔧 配置选项

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

## 📊 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 搜索响应时间 | <20ms | 语义搜索平均时间 |
| Token 节省 | 70-90% | 相比完整上下文 |
| 记忆容量 | 10,000+ | 支持的最大记忆数量 |
| 内存使用 | <100MB | 典型工作负载 |

## 🤝 贡献

欢迎贡献！请阅读 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 📞 支持

- **问题报告**: [GitHub Issues](https://github.com/yourusername/three-component-memory-system/issues)
- **文档**: [docs/](docs/)
- **讨论**: [GitHub Discussions](https://github.com/yourusername/three-component-memory-system/discussions)

---

**三组件记忆系统** - 让 AI 助手拥有真正的长期记忆

---

**最新版本**: 1.2.0 (2026-03-19)  
**更新日志**: [English](CHANGELOG.md) | [中文](CHANGELOG_zh.md)  
**状态**: 生产就绪（基于skill-creator优化）