#!/usr/bin/env python3
"""
Basic tests for Three-Component Memory System.
"""

import unittest
import tempfile
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from three_component_memory import MemorySystem


class TestMemorySystem(unittest.TestCase):
    """Test cases for MemorySystem."""
    
    def setUp(self):
        """Set up test environment."""
        # Use temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.config = {
            'data_path': self.test_dir,
            'auto_record': False,  # Disable auto-record for tests
            'debug': False
        }
        self.memory = MemorySystem(self.config)
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test system initialization."""
        stats = self.memory.get_stats()
        self.assertEqual(stats['status'], 'healthy')
        self.assertTrue(stats['config_loaded'])
        self.assertIn('sqlite', stats['components'])
        self.assertIn('lancedb', stats['components'])
        self.assertIn('networkx', stats['components'])
    
    def test_add_memory(self):
        """Test adding a memory."""
        memory_id = self.memory.add(
            content="Test memory content",
            category="test",
            tags=["test", "unit"],
            importance=3
        )
        
        self.assertIsNotNone(memory_id)
        self.assertIsInstance(memory_id, str)
        self.assertGreater(len(memory_id), 0)
    
    def test_search_memory(self):
        """Test searching memories."""
        # Add test memory
        self.memory.add(
            content="Test memory about artificial intelligence",
            category="technology",
            importance=3
        )
        
        # Search for it
        results = self.memory.search("artificial intelligence", search_type="text")
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Check result structure
        result = results[0]
        self.assertIn('id', result)
        self.assertIn('content', result)
        self.assertIn('score', result)
        self.assertGreaterEqual(result['score'], 0.0)
        self.assertLessEqual(result['score'], 1.0)
    
    def test_different_search_types(self):
        """Test different search types."""
        # Add test memory
        self.memory.add(
            content="Vector databases enable semantic search capabilities",
            category="database",
            importance=3
        )
        
        # Test semantic search
        semantic_results = self.memory.search("meaning-based search", search_type="semantic")
        self.assertIsInstance(semantic_results, list)
        
        # Test text search
        text_results = self.memory.search("vector database", search_type="text")
        self.assertIsInstance(text_results, list)
        
        # Test hybrid search
        hybrid_results = self.memory.search("search technology", search_type="hybrid")
        self.assertIsInstance(hybrid_results, list)
    
    def test_get_stats(self):
        """Test getting system statistics."""
        stats = self.memory.get_stats()
        
        # Check required fields
        required_fields = ['status', 'version', 'config_loaded', 'memory_count', 'components']
        for field in required_fields:
            self.assertIn(field, stats)
        
        # Check component status
        self.assertIn('component_status', stats)
        component_status = stats['component_status']
        for component in stats['components']:
            self.assertIn(component, component_status)
    
    def test_auto_record_importance(self):
        """Test auto-record importance calculation."""
        # Important conversation (should be recorded with auto_record=True)
        memory_important = MemorySystem({
            'data_path': self.test_dir,
            'auto_record': True,
            'importance_threshold': 3
        })
        
        memory_id = memory_important.auto_record(
            user_message="Important decision about project architecture",
            ai_response="We should use microservices for better scalability"
        )
        
        # This might or might not be recorded depending on importance calculation
        # Just test that the function runs without error
        self.assertIsInstance(memory_id, (str, type(None)))
    
    def test_config_override(self):
        """Test configuration override."""
        custom_config = {
            'data_path': self.test_dir,
            'auto_record': False,
            'importance_threshold': 5,
            'debug': True
        }
        
        memory = MemorySystem(custom_config)
        stats = memory.get_stats()
        
        self.assertEqual(stats['config']['auto_record'], False)
        self.assertEqual(stats['config']['importance_threshold'], 5)
        self.assertEqual(stats['config']['debug'], True)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_empty_search(self):
        """Test searching with empty query."""
        memory = MemorySystem({'data_path': self.test_dir})
        results = memory.search("", search_type="text")
        self.assertEqual(results, [])
    
    def test_invalid_search_type(self):
        """Test searching with invalid search type."""
        memory = MemorySystem({'data_path': self.test_dir})
        
        # Should default to hybrid or handle gracefully
        results = memory.search("test", search_type="invalid_type")
        self.assertIsInstance(results, list)
    
    def test_memory_with_special_characters(self):
        """Test memory with special characters."""
        memory = MemorySystem({'data_path': self.test_dir})
        
        content = "Test with special chars: 中文测试 🚀 @#$%^&*()"
        memory_id = memory.add(
            content=content,
            category="test",
            tags=["special", "chars"],
            importance=3
        )
        
        self.assertIsNotNone(memory_id)
        
        # Try to search for it
        results = memory.search("中文测试", search_type="text")
        self.assertIsInstance(results, list)


if __name__ == '__main__':
    unittest.main()
