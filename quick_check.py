#!/usr/bin/env python3
"""
Quick local smoke test for the Three-Component Memory System.

用来在本地快速验证：
- 模块能否导入
- MemorySystem 能否初始化
- 基本 add/search 是否工作

用法：
    python3 quick_check.py
"""

import os
import sys
import tempfile


def main() -> int:
    # 确保 src 在导入路径中（和 tests 里的做法保持一致）
    repo_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(repo_root, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    try:
        from three_component_memory import MemorySystem, __version__  # type: ignore
    except Exception as e:
        print(f"❌ 无法导入 three_component_memory: {e}")
        return 1

    print(f"✅ 模块导入成功，版本: {__version__}")

    tmp_dir = tempfile.mkdtemp(prefix="three-component-memory-quickcheck-")
    print(f"🧪 使用临时数据目录: {tmp_dir}")

    try:
        memory = MemorySystem(
            {
                "data_path": tmp_dir,
                "debug": False,
                "auto_record": False,
            }
        )

        stats = memory.get_stats()
        print(f"✅ 初始化成功，状态: {stats.get('status', 'unknown')}")
        print(f"   组件: {stats.get('components', [])}")

        # 测试添加一条内存
        mem_id = memory.add(
            content="Quick check: 三组件记忆系统本地自测",
            category="quickcheck",
            importance=2,
            tags=["quickcheck", "local"],
        )
        if not mem_id:
            print("⚠️ 添加内存返回 None，可能是内部出错（详见 debug 日志）")
        else:
            print(f"✅ 内存添加成功，ID: {mem_id}")

        # 测试一次简单搜索（在最小实现下，语义部分可能返回空）
        results = memory.search("自测", search_type="text")
        print(f"✅ 搜索完成，返回 {len(results)} 条结果（text 模式）")

        return 0

    except Exception as e:
        print(f"❌ quick_check 过程中出错: {e}")
        return 1
    finally:
        # 清理临时目录
        import shutil

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())

