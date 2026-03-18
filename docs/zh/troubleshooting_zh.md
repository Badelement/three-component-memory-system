# 故障排除指南

## 快速诊断

### 系统状态检查
```bash
# 运行诊断脚本
python scripts/diagnose.py

# 或手动检查
python -c "
import sys
sys.path.insert(0, 'src')
from three_component_memory import MemorySystem
try:
    memory = MemorySystem()
    stats = memory.get_stats()
    print('✅ 系统状态:', stats.get('status', 'unknown'))
    print('✅ 记忆数量:', stats.get('memory_count', 0))
except Exception as e:
    print('❌ 错误:', e)
"
```

## 常见问题

### 安装问题

#### 问题：导入时出现 ImportError
```
ModuleNotFoundError: No module named 'three_component_memory'
```

**原因:**
1. 技能目录不在 Python 路径中
2. 缺少 __init__.py 文件
3. 模块名称不正确

**解决方案:**
1. 检查技能目录是否存在：
   ```bash
   ls -la ~/.openclaw/skills/three-component-memory/
   ```

2. 验证 Python 路径包含该目录：
   ```python
   import sys
   sys.path.insert(0, "/Users/yourusername/.openclaw/skills/three-component-memory")
   from __init__ import MemorySystem
   ```

3. 重新安装技能：
   ```bash
   cd /path/to/three-component-memory-system
   ./scripts/setup_env.sh
   ```

#### 问题：依赖安装失败
```
pip install lancedb networkx sentence-transformers 失败
```

**原因:**
1. Python 版本不兼容
2. 网络连接问题
3. 系统依赖缺失

**解决方案:**
1. 检查 Python 版本：
   ```bash
   python --version  # 需要 3.8+
   ```

2. 使用国内镜像源：
   ```bash
   pip install lancedb networkx sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. 安装系统依赖（Ubuntu/Debian）：
   ```bash
   sudo apt-get update
   sudo apt-get install python3-dev build-essential
   ```

### 配置问题

#### 问题：OpenClaw 无法识别技能
```
openclaw skills list 中看不到 three-component-memory
```

**原因:**
1. 技能目录位置不正确
2. 配置未启用
3. OpenClaw 配置未重新加载

**解决方案:**
1. 检查技能目录位置：
   ```bash
   # 正确位置
   ~/.openclaw/skills/three-component-memory/
   
   # 检查目录结构
   ls ~/.openclaw/skills/three-component-memory/SKILL.md
   ```

2. 验证 OpenClaw 配置：
   ```bash
   openclaw config get skills.three-component-memory
   ```

3. 重启 OpenClaw Gateway：
   ```bash
   openclaw gateway restart
   ```

#### 问题：自动记录不工作
```
对话内容没有被自动记录
```

**原因:**
1. `auto_record` 配置为 false
2. `importance_threshold` 设置过高
3. 重要性评估逻辑问题

**解决方案:**
1. 检查配置：
   ```bash
   openclaw config get skills.three-component-memory.auto_record
   openclaw config get skills.three-component-memory.importance_threshold
   ```

2. 调整配置：
   ```bash
   openclaw config set skills.three-component-memory.auto_record true
   openclaw config set skills.three-component-memory.importance_threshold 2
   ```

3. 测试重要性评估：
   ```python
   from three_component_memory.utils.importance import assess_importance
   
   text = "这是一个重要的项目决策"
   importance = assess_importance(text)
   print(f"重要性评分: {importance}")
   ```

### 性能问题

#### 问题：搜索速度慢
```
语义搜索需要很长时间
```

**原因:**
1. 向量索引未优化
2. 记忆数量过多
3. 硬件资源不足

**解决方案:**
1. 重建向量索引：
   ```python
   memory = MemorySystem()
   memory.rebuild_index()
   ```

2. 限制搜索范围：
   ```python
   # 使用更具体的搜索
   results = memory.search("具体查询", limit=5)
   
   # 按分类筛选
   results = memory.search("查询", category="特定分类")
   ```

3. 检查系统资源：
   ```bash
   # 检查内存使用
   free -h
   
   # 检查CPU使用
   top
   ```

#### 问题：内存使用过高
```
系统占用大量内存
```

**原因:**
1. 记忆缓存过大
2. 图数据结构未优化
3. 内存泄漏

**解决方案:**
1. 调整缓存大小：
   ```python
   memory.update_config("cache_size", 1000)  # 限制缓存条目
   ```

2. 清理旧记忆：
   ```python
   memory.cleanup(max_age_days=30, min_importance=2)
   ```

3. 重启系统释放内存：
   ```bash
   openclaw gateway restart
   ```

### 数据问题

#### 问题：记忆丢失
```
之前添加的记忆不见了
```

**原因:**
1. 数据文件损坏
2. 存储路径更改
3. 清理操作误删

**解决方案:**
1. 检查数据文件：
   ```bash
   ls -la ~/.openclaw/memory/three_component/
   ```

2. 从备份恢复：
   ```python
   memory = MemorySystem()
   memory.restore("~/backups/memory_backup.zip")
   ```

3. 检查清理配置：
   ```bash
   openclaw config get skills.three-component-memory.cleanup_interval
   ```

#### 问题：搜索返回无关结果
```
搜索结果与查询不相关
```

**原因:**
1. 向量模型不匹配
2. 嵌入质量差
3. 搜索参数不当

**解决方案:**
1. 尝试不同搜索类型：
   ```python
   # 语义搜索
   results = memory.search("查询", search_type="semantic")
   
   # 文本搜索
   results = memory.search("查询", search_type="text")
   
   # 混合搜索
   results = memory.search("查询", search_type="hybrid")
   ```

2. 调整搜索参数：
   ```python
   # 增加相似度阈值
   results = memory.search("查询", min_similarity=0.7)
   
   # 限制结果数量
   results = memory.search("查询", limit=5)
   ```

3. 重新训练嵌入（高级）：
   ```python
   memory.retrain_embeddings()
   ```

### 集成问题

#### 问题：OpenClaw 命令不工作
```
/memory 命令无响应
```

**原因:**
1. 技能未正确注册
2. 命令处理器故障
3. 权限问题

**解决方案:**
1. 检查技能注册：
   ```bash
   openclaw skills info three-component-memory
   ```

2. 查看 OpenClaw 日志：
   ```bash
   tail -f ~/.openclaw/logs/gateway.err.log
   ```

3. 重新注册技能：
   ```bash
   openclaw skills reload
   ```

#### 问题：与其他技能冲突
```
多个记忆相关技能冲突
```

**原因:**
1. 命令前缀冲突
2. 数据文件冲突
3. 资源竞争

**解决方案:**
1. 修改命令前缀：
   ```json
   {
     "skills": {
       "three-component-memory": {
         "command_prefix": "mem3"  # 改为 mem3 避免冲突
       }
     }
   }
   ```

2. 使用独立数据目录：
   ```json
   {
     "skills": {
       "three-component-memory": {
         "data_path": "~/.openclaw/memory/three_component_v2/"
       }
     }
   }
   ```

3. 禁用冲突技能：
   ```bash
   openclaw config set skills.other-memory-system.enabled false
   ```

## 高级故障排除

### 调试模式

启用调试日志以获取详细信息：

```python
memory = MemorySystem({"debug": True})
```

或通过 OpenClaw 配置：
```bash
openclaw config set skills.three-component-memory.debug true
openclaw gateway restart
```

### 组件级诊断

检查各个组件状态：

```python
from three_component_memory import MemorySystem

memory = MemorySystem()

# 检查 LanceDB
lance_status = memory._check_lancedb()
print(f"LanceDB 状态: {lance_status}")

# 检查 SQLite
sqlite_status = memory._check_sqlite()
print(f"SQLite 状态: {sqlite_status}")

# 检查 NetworkX
networkx_status = memory._check_networkx()
print(f"NetworkX 状态: {networkx_status}")
```

### 性能分析

使用性能分析工具：

```python
import cProfile
from three_component_memory import MemorySystem

memory = MemorySystem()

# 分析搜索性能
profiler = cProfile.Profile()
profiler.enable()

# 执行搜索操作
results = memory.search("测试查询", search_type="semantic")

profiler.disable()
profiler.print_stats(sort='time')
```

## 获取帮助

如果以上解决方案都无法解决问题：

1. **检查日志文件**：
   ```bash
   # OpenClaw 日志
   tail -100 ~/.openclaw/logs/gateway.err.log
   
   # 技能日志
   tail -100 ~/.openclaw/memory/three_component/logs/system.log
   ```

2. **创建诊断报告**：
   ```bash
   python scripts/diagnose.py --report > diagnosis_report.txt
   ```

3. **提交 Issue**：
   - 包含诊断报告
   - 描述复现步骤
   - 提供相关日志
   - [GitHub Issues](https://github.com/yourusername/three-component-memory-system/issues)

4. **社区支持**：
   - [GitHub Discussions](https://github.com/yourusername/three-component-memory-system/discussions)
   - OpenClaw Discord 社区

## 预防措施

### 定期维护
1. **定期备份**：
   ```python
   memory.backup()
   ```

2. **定期清理**：
   ```python
   memory.cleanup(max_age_days=90)
   ```

3. **定期优化**：
   ```python
   memory.optimize()
   ```

### 监控配置
1. **设置监控告警**：
   ```bash
   # 检查记忆数量
   python -c "
   from three_component_memory import MemorySystem
   memory = MemorySystem()
   stats = memory.get_stats()
   if stats['total_memories'] > 10000:
       print('警告: 记忆数量超过阈值')
   "
   ```

2. **性能基线**：
   ```bash
   # 记录正常性能指标
   python scripts/benchmark.py --save-baseline
   ```

### 更新策略
1. **定期更新**：
   ```bash
   git pull origin main
   pip install --upgrade -r requirements.txt
   ```

2. **测试更新**：
   ```bash
   python -m pytest tests/ -v
   ```

---

**重要提示**: 在进行任何重大更改前，请务必备份数据。