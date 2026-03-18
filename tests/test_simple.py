#!/usr/bin/env python3
"""
简化测试 - 用于CI/CD环境
"""

import unittest
import tempfile
import os
import sys

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestSimpleImport(unittest.TestCase):
    """测试基本导入和初始化"""
    
    def test_import(self):
        """测试模块导入"""
        try:
            from three_component_memory import MemorySystem, __version__
            self.assertIsNotNone(__version__)
            print(f"✅ 导入成功 v{__version__}")
        except ImportError as e:
            # 在CI环境中，如果缺少重依赖，跳过测试
            import os
            if os.getenv('SKIP_HEAVY_DEPS') == 'true':
                self.skipTest(f"跳过重依赖测试: {e}")
            else:
                raise
    
    def test_basic_initialization(self):
        """测试基本初始化"""
        from three_component_memory import MemorySystem
        
        # 使用临时目录
        test_dir = tempfile.mkdtemp()
        
        try:
            memory = MemorySystem({
                'data_path': test_dir,
                'debug': False,
                'auto_record': False
            })
            
            stats = memory.get_stats()
            self.assertIn('status', stats)
            self.assertIn('config_loaded', stats)
            print(f"✅ 初始化成功: {stats['status']}")
            
        finally:
            import shutil
            shutil.rmtree(test_dir)
    
    def test_memory_operations(self):
        """测试基本内存操作"""
        from three_component_memory import MemorySystem
        
        test_dir = tempfile.mkdtemp()
        
        try:
            memory = MemorySystem({
                'data_path': test_dir,
                'debug': False,
                'auto_record': False
            })
            
            # 测试添加内存
            memory_id = memory.add(
                content="Test memory content",
                category="test",
                importance=1
            )
            
            self.assertIsNotNone(memory_id)
            self.assertIsInstance(memory_id, str)
            print(f"✅ 内存添加成功: {memory_id}")
            
            # 测试搜索（可能没有实际数据，但应该不报错）
            results = memory.search("test", search_type="text")
            self.assertIsInstance(results, list)
            print(f"✅ 搜索返回 {len(results)} 个结果")
            
        finally:
            import shutil
            shutil.rmtree(test_dir)


class TestConfiguration(unittest.TestCase):
    """测试配置"""
    
    def test_config_override(self):
        """测试配置覆盖"""
        from three_component_memory import MemorySystem
        
        test_dir = tempfile.mkdtemp()
        
        try:
            custom_config = {
                'data_path': test_dir,
                'auto_record': False,
                'importance_threshold': 5,
                'debug': True
            }
            
            memory = MemorySystem(custom_config)
            stats = memory.get_stats()
            
            self.assertEqual(stats['config']['auto_record'], False)
            self.assertEqual(stats['config']['importance_threshold'], 5)
            print("✅ 配置覆盖成功")
            
        finally:
            import shutil
            shutil.rmtree(test_dir)


if __name__ == '__main__':
    # 简单运行测试
    import sys
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    sys.exit(0 if result.wasSuccessful() else 1)
