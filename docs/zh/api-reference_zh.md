# API 参考

## MemorySystem 类

### 构造函数
```python
MemorySystem(config=None)
```

初始化记忆系统。

**参数:**
- `config` (dict, 可选): 配置字典
  - `auto_record` (bool): 启用自动记录（默认: True）
  - `importance_threshold` (int): 记录的最小重要性（1-5，默认: 3）
  - `data_path` (str): 数据目录路径
  - `debug` (bool): 启用调试日志（默认: False）

**示例:**
```python
from three_component_memory import MemorySystem

# 默认配置
memory = MemorySystem()

# 自定义配置
memory = MemorySystem({
    "auto_record": True,
    "importance_threshold": 4,
    "data_path": "~/custom/path",
    "debug": True
})
```

## 核心方法

### add()
```python
add(content, category="general", tags=None, importance=3, metadata=None)
```

向系统添加新记忆。

**参数:**
- `content` (str): 记忆内容文本
- `category` (str): 分类名称（默认: "general"）
- `tags` (list): 标签字符串列表（默认: []）
- `importance` (int): 重要性级别 1-5（默认: 3）
- `metadata` (dict): 额外元数据（默认: {}）

**返回:**
- `str`: 新创建记忆的 ID

**示例:**
```python
memory_id = memory.add(
    content="项目决定：采用微服务架构",
    category="项目",
    tags=["架构", "决策", "微服务"],
    importance=5,
    metadata={"source": "会议记录", "participants": ["Alice", "Bob"]}
)
```

### search()
```python
search(query, search_type="semantic", limit=10, category=None, min_importance=None)
```

搜索记忆。

**参数:**
- `query` (str): 搜索查询文本
- `search_type` (str): 搜索类型，可选 "semantic"（语义）、"text"（文本）、"hybrid"（混合）（默认: "semantic"）
- `limit` (int): 返回结果数量限制（默认: 10）
- `category` (str): 按分类筛选（可选）
- `min_importance` (int): 最小重要性筛选（可选）

**返回:**
- `list`: 记忆对象列表，按相关性排序

**示例:**
```python
# 语义搜索
results = memory.search("微服务设计模式", search_type="semantic")

# 文本搜索
results = memory.search("架构 决策", search_type="text")

# 混合搜索
results = memory.search("项目规划", search_type="hybrid", limit=5)

# 带筛选的搜索
results = memory.search(
    "技术决策",
    category="项目",
    min_importance=4,
    limit=8
)
```

### get()
```python
get(memory_id)
```

按 ID 获取特定记忆。

**参数:**
- `memory_id` (str): 记忆 ID

**返回:**
- `dict`: 记忆对象，包含所有字段

**示例:**
```python
mem = memory.get("mem_123456")
print(f"内容: {mem['content']}")
print(f"分类: {mem['category']}")
print(f"重要性: {mem['importance']}")
```

### update()
```python
update(memory_id, updates)
```

更新现有记忆。

**参数:**
- `memory_id` (str): 要更新的记忆 ID
- `updates` (dict): 要更新的字段

**返回:**
- `bool`: 更新是否成功

**示例:**
```python
success = memory.update("mem_123456", {
    "importance": 5,
    "tags": ["架构", "决策", "重要"],
    "metadata": {"updated_by": "admin"}
})
```

### delete()
```python
delete(memory_id)
```

删除记忆。

**参数:**
- `memory_id` (str): 要删除的记忆 ID

**返回:**
- `bool`: 删除是否成功

**示例:**
```python
success = memory.delete("mem_123456")
```

## 查询方法

### get_by_category()
```python
get_by_category(category, limit=50, offset=0)
```

按分类获取记忆。

**参数:**
- `category` (str): 分类名称
- `limit` (int): 返回数量限制（默认: 50）
- `offset` (int): 偏移量（默认: 0）

**返回:**
- `list`: 记忆对象列表

**示例:**
```python
project_memories = memory.get_by_category("项目", limit=20)
```

### get_by_tag()
```python
get_by_tag(tag, limit=50, offset=0)
```

按标签获取记忆。

**参数:**
- `tag` (str): 标签名称
- `limit` (int): 返回数量限制（默认: 50）
- `offset` (int): 偏移量（默认: 0）

**返回:**
- `list`: 记忆对象列表

**示例:**
```python
architecture_memories = memory.get_by_tag("架构")
```

### get_recent()
```python
get_recent(limit=20, offset=0)
```

获取最近的记忆。

**参数:**
- `limit` (int): 返回数量限制（默认: 20）
- `offset` (int): 偏移量（默认: 0）

**返回:**
- `list`: 记忆对象列表，按时间倒序

**示例:**
```python
recent_memories = memory.get_recent(limit=10)
```

### get_important()
```python
get_important(min_importance=4, limit=20, offset=0)
```

获取重要记忆。

**参数:**
- `min_importance` (int): 最小重要性（默认: 4）
- `limit` (int): 返回数量限制（默认: 20）
- `offset` (int): 偏移量（默认: 0）

**返回:**
- `list`: 记忆对象列表

**示例:**
```python
important_memories = memory.get_important(min_importance=5, limit=15)
```

## 统计方法

### get_stats()
```python
get_stats()
```

获取系统统计信息。

**返回:**
- `dict`: 统计信息字典

**示例:**
```python
stats = memory.get_stats()
print(f"总记忆数: {stats['total_memories']}")
print(f"分类统计: {stats['categories']}")
print(f"标签统计: {stats['tags']}")
print(f"平均重要性: {stats['avg_importance']:.2f}")
```

### get_category_stats()
```python
get_category_stats()
```

获取分类统计信息。

**返回:**
- `dict`: 分类统计字典

**示例:**
```python
category_stats = memory.get_category_stats()
for category, count in category_stats.items():
    print(f"{category}: {count} 条记忆")
```

### get_tag_stats()
```python
get_tag_stats()
```

获取标签统计信息。

**返回:**
- `dict`: 标签统计字典

**示例:**
```python
tag_stats = memory.get_tag_stats()
for tag, count in tag_stats.items():
    print(f"#{tag}: {count} 次使用")
```

## 关系方法

### find_related()
```python
find_related(memory_id, max_distance=2, limit=10)
```

查找相关记忆。

**参数:**
- `memory_id` (str): 源记忆 ID
- `max_distance` (int): 最大关系距离（默认: 2）
- `limit` (int): 返回数量限制（默认: 10）

**返回:**
- `list`: 相关记忆列表，包含关系信息

**示例:**
```python
related = memory.find_related("mem_123456", max_distance=3)
for mem in related:
    print(f"相关记忆: {mem['content'][:50]}...")
    print(f"关系类型: {mem['relationship']}")
    print(f"距离: {mem['distance']}")
```

### get_community()
```python
get_community(memory_id)
```

获取记忆所属的社区（聚类）。

**参数:**
- `memory_id` (str): 记忆 ID

**返回:**
- `list`: 同一社区的记忆 ID 列表

**示例:**
```python
community = memory.get_community("mem_123456")
print(f"社区大小: {len(community)} 条记忆")
```

### get_central_memories()
```python
get_central_memories(limit=10)
```

获取中心性最高的记忆（最重要的连接节点）。

**参数:**
- `limit` (int): 返回数量限制（默认: 10）

**返回:**
- `list`: 中心记忆列表

**示例:**
```python
central = memory.get_central_memories(limit=5)
for mem in central:
    print(f"中心记忆: {mem['content'][:60]}...")
    print(f"中心性分数: {mem['centrality']:.3f}")
```

## 配置方法

### update_config()
```python
update_config(key, value)
```

更新系统配置。

**参数:**
- `key` (str): 配置键
- `value`: 配置值

**返回:**
- `bool`: 更新是否成功

**示例:**
```python
memory.update_config("importance_threshold", 4)
memory.update_config("auto_record", False)
```

### get_config()
```python
get_config()
```

获取当前配置。

**返回:**
- `dict`: 配置字典

**示例:**
```python
config = memory.get_config()
print(f"当前配置: {config}")
```

## 维护方法

### cleanup()
```python
cleanup(max_age_days=30, min_importance=1)
```

清理旧的和不重要的记忆。

**参数:**
- `max_age_days` (int): 最大保留天数（默认: 30）
- `min_importance` (int): 保留的最小重要性（默认: 1）

**返回:**
- `dict`: 清理统计信息

**示例:**
```python
cleanup_stats = memory.cleanup(max_age_days=90, min_importance=2)
print(f"清理了 {cleanup_stats['deleted']} 条记忆")
print(f"保留了 {cleanup_stats['kept']} 条记忆")
```

### backup()
```python
backup(backup_path=None)
```

创建系统备份。

**参数:**
- `backup_path` (str): 备份路径（可选）

**返回:**
- `str`: 备份文件路径

**示例:**
```python
backup_file = memory.backup("~/backups/memory_backup.zip")
print(f"备份已创建: {backup_file}")
```

### restore()
```python
restore(backup_file)
```

从备份恢复系统。

**参数:**
- `backup_file` (str): 备份文件路径

**返回:**
- `bool`: 恢复是否成功

**示例:**
```python
success = memory.restore("~/backups/memory_backup_20250318.zip")
```

## 高级功能

### batch_add()
```python
batch_add(memories)
```

批量添加记忆。

**参数:**
- `memories` (list): 记忆字典列表

**返回:**
- `list`: 创建的记忆 ID 列表

**示例:**
```python
memories_to_add = [
    {
        "content": "决策1: 使用Docker容器化",
        "category": "技术",
        "importance": 4
    },
    {
        "content": "决策2: 采用CI/CD流水线",
        "category": "流程",
        "importance": 5
    }
]

memory_ids = memory.batch_add(memories_to_add)
```

### export_memories()
```python
export_memories(format="json", filepath=None)
```

导出记忆。

**参数:**
- `format` (str): 导出格式，可选 "json"、"csv"、"markdown"（默认: "json"）
- `filepath` (str): 导出文件路径（可选）

**返回:**
- `str` 或 `list`: 导出数据或文件路径

**示例:**
```python
# 导出为JSON
json_data = memory.export_memories(format="json")

# 导出为CSV文件
csv_file = memory.export_memories(format="csv", filepath="memories.csv")

# 导出为Markdown
md_content = memory.export_memories(format="markdown")
```

### import_memories()
```python
import_memories(data, format="json")
```

导入记忆。

**参数:**
- `data`: 导入数据（文件路径或数据对象）
- `format` (str): 数据格式，可选 "json"、"csv"（默认: "json"）

**返回:**
- `dict`: 导入统计信息

**示例:**
```python
# 从JSON文件导入
stats = memory.import_memories("memories_backup.json", format="json")

# 从CSV文件导入
stats = memory.import_memories("memories.csv", format="csv")

print(f"导入了 {stats['imported']} 条记忆")
print(f"跳过了 {stats['skipped']} 条重复记忆")
```

---

**注意**: 所有方法都包含适当的错误处理，并在发生错误时返回 `None` 或引发适当的异常。