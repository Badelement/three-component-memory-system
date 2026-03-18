# 快速开始

本指南将帮助您安装并开始使用三组件记忆系统。

## 前提条件

- **Python 3.8 或更高版本**
- **OpenClaw** 已安装并运行
- **Git**（用于克隆仓库）

## 安装方法

### 方法一：快速安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/yourusername/three-component-memory-system.git
cd three-component-memory-system

# 运行安装脚本
./scripts/setup_env.sh
```

安装脚本将执行以下操作：
1. 检查系统要求
2. 安装 Python 依赖
3. 配置 OpenClaw
4. 测试安装

### 方法二：手动安装

#### 步骤 1：安装依赖
```bash
pip install lancedb networkx sentence-transformers numpy
```

#### 步骤 2：安装技能
```bash
# 克隆或下载仓库
git clone https://github.com/yourusername/three-component-memory-system.git

# 复制到 OpenClaw skills 目录
mkdir -p ~/.openclaw/skills/
cp -r three-component-memory-system/src ~/.openclaw/skills/three-component-memory
```

#### 步骤 3：配置 OpenClaw

编辑 `~/.openclaw/config.json` 并添加：

```json
{
  "skills": {
    "three-component-memory": {
      "enabled": true,
      "auto_record": true,
      "importance_threshold": 3,
      "vector_model": "all-MiniLM-L6-v2",
      "max_memories": 10000,
      "search_limit": 10
    }
  }
}
```

#### 步骤 4：重启 OpenClaw
```bash
openclaw gateway restart
```

## 验证安装

### 检查技能状态
```bash
# 查看技能列表
openclaw skills list

# 应该能看到 three-component-memory 技能
```

### 运行测试
```bash
# 运行系统测试
python -m pytest tests/ -v

# 或运行快速检查
python quick_check.py
```

## 基本使用

### 通过 OpenClaw 使用

安装后，您可以在 OpenClaw 中使用以下命令：

```
# 搜索记忆
/memory search "项目规划" --type semantic

# 查看统计信息
/memory stats

# 添加记忆
/memory add "重要决定：使用微服务架构" --category project --importance 4

# 配置系统
/memory config auto_record true
```

### 通过 Python API 使用

```python
from three_component_memory import MemorySystem

# 初始化系统
memory = MemorySystem()

# 添加记忆
memory.add(
    content="项目决策：采用微服务架构",
    category="项目",
    importance=5,
    tags=["架构", "决策"]
)

# 搜索记忆
results = memory.search("微服务设计", search_type="semantic")
for mem in results:
    print(f"相关记忆: {mem.content}")
    print(f"相似度: {mem.score:.3f}")
    print(f"时间: {mem.timestamp}")
    print("---")

# 查看统计信息
stats = memory.get_stats()
print(f"总记忆数: {stats['total_memories']}")
print(f"分类统计: {stats['categories']}")
```

## 配置选项

### 核心配置

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `enabled` | boolean | `true` | 启用/禁用技能 |
| `auto_record` | boolean | `true` | 自动记录重要对话 |
| `importance_threshold` | integer | `3` | 自动记录的重要性阈值（1-5） |
| `vector_model` | string | `"all-MiniLM-L6-v2"` | 向量嵌入模型 |
| `max_memories` | integer | `10000` | 最大记忆数量 |
| `search_limit` | integer | `10` | 搜索结果限制 |

### 高级配置

```json
{
  "skills": {
    "three-component-memory": {
      "enabled": true,
      "auto_record": true,
      "importance_threshold": 3,
      "vector_model": "all-MiniLM-L6-v2",
      "max_memories": 10000,
      "search_limit": 10,
      "cleanup_interval": 86400,
      "backup_enabled": true,
      "backup_path": "~/.openclaw/memory/backups/"
    }
  }
}
```

## 下一步

- 查看 [API 参考](api-reference_zh.md) 了解完整功能
- 阅读 [架构设计](architecture_zh.md) 理解系统原理
- 参考 [故障排除](troubleshooting_zh.md) 解决常见问题
- 查看 [示例代码](../examples/) 获取使用灵感

## 获取帮助

如果您遇到问题：

1. 检查 [故障排除指南](troubleshooting_zh.md)
2. 查看 [GitHub Issues](https://github.com/yourusername/three-component-memory-system/issues)
3. 在 [GitHub Discussions](https://github.com/yourusername/three-component-memory-system/discussions) 提问

---

**提示**：首次使用建议从少量记忆开始，逐步增加复杂度。