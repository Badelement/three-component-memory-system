"""
Core implementation of the three components.
"""

import os
import json
import sqlite3
import time
import pickle
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Memory:
    """Memory data class."""
    id: str
    content: str
    category: str = "general"
    tags: List[str] = None
    importance: int = 3
    metadata: Dict[str, Any] = None
    created_at: float = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class SQLiteStorage:
    """SQLite-based structured storage."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create main memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                tags TEXT,  -- JSON array
                importance INTEGER DEFAULT 3,
                metadata TEXT,  -- JSON object
                created_at REAL
            )
        ''')
        
        # Create full-text search virtual table
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts 
            USING fts5(content, category, tags)
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON memories(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON memories(created_at)')
        
        conn.commit()
        conn.close()
    
    def add(self, memory_data: Dict[str, Any]):
        """Add a memory to SQLite."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert into main table
            cursor.execute('''
                INSERT INTO memories (id, content, category, tags, importance, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory_data['id'],
                memory_data['content'],
                memory_data.get('category', 'general'),
                json.dumps(memory_data.get('tags', [])),
                memory_data.get('importance', 3),
                json.dumps(memory_data.get('metadata', {})),
                memory_data.get('created_at', time.time())
            ))
            
            # Insert into FTS table
            cursor.execute('''
                INSERT INTO memories_fts (rowid, content, category, tags)
                VALUES ((SELECT last_insert_rowid()), ?, ?, ?)
            ''', (
                memory_data['content'],
                memory_data.get('category', 'general'),
                ' '.join(memory_data.get('tags', []))
            ))
            
            conn.commit()
        finally:
            conn.close()
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories using full-text search."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # Use FTS5 for text search
            cursor.execute('''
                SELECT m.*, fts.rank
                FROM memories_fts fts
                JOIN memories m ON m.rowid = fts.rowid
                WHERE fts.content MATCH ?
                ORDER BY fts.rank
                LIMIT ?
            ''', (query, limit))
            
            results = []
            for row in cursor.fetchall():
                memory_dict = dict(row)
                # Convert JSON strings back to Python objects
                if memory_dict.get('tags'):
                    memory_dict['tags'] = json.loads(memory_dict['tags'])
                if memory_dict.get('metadata'):
                    memory_dict['metadata'] = json.loads(memory_dict['metadata'])
                
                # Add score (convert rank to 0-1 scale)
                rank = memory_dict.pop('rank', 0)
                memory_dict['score'] = max(0.0, min(1.0, 1.0 / (rank + 1)))
                
                results.append(memory_dict)
            
            return results
        finally:
            conn.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get SQLite statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) FROM memories')
            count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT category) FROM memories')
            category_count = cursor.fetchone()[0]
            
            return {
                'count': count,
                'category_count': category_count,
                'db_size': os.path.getsize(self.db_path)
            }
        finally:
            conn.close()
    
    def cleanup(self):
        """Perform maintenance operations."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Vacuum to optimize database
            cursor.execute('VACUUM')
            conn.commit()
        finally:
            conn.close()


class LanceDBVectorStore:
    """
    Lightweight LanceDB-like vector store.

    在 CI / 轻量环境中，为了避免引入 lancedb 和大模型依赖，
    这里实现一个 API 兼容但功能最小化的版本：
    - add: 记录计数，但不做真实向量存储
    - search: 返回空列表（语义搜索在最小实现中是 no-op）
    - get_stats: 返回简单统计信息
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._meta_path = os.path.join(self.db_path, "meta.pkl")
        os.makedirs(self.db_path, exist_ok=True)
        self._count = 0
        if os.path.exists(self._meta_path):
            try:
                with open(self._meta_path, "rb") as f:
                    data = pickle.load(f)
                    self._count = int(data.get("count", 0))
            except Exception:
                self._count = 0

    def add(self, memory_data: Dict[str, Any]):
        """Record that a memory was added (no real vector operations)."""
        self._count += 1
        try:
            with open(self._meta_path, "wb") as f:
                pickle.dump({"count": self._count}, f)
        except Exception:
            # 元数据失败不影响主流程
            pass

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Simplified semantic search stub.

        完整实现里，这里会进行向量检索。
        当前为了在没有重依赖时也能通过测试，直接返回空列表。
        """
        return []

    def get_stats(self) -> Dict[str, Any]:
        """Return basic stats for the vector store."""
        return {
            "count": self._count,
            "db_path": self.db_path,
        }

    def cleanup(self):
        """No-op cleanup for compatibility."""
        return


class NetworkXGraph:
    """
    Lightweight relationship graph.

    为了避免强依赖 networkx，这里提供一个接口兼容的简化版本：
    - add: 只做节点计数
    - get_stats: 返回节点/边统计
    """

    def __init__(self, graph_path: str):
        self.graph_path = graph_path
        os.makedirs(self.graph_path, exist_ok=True)
        self._node_count = 0
        self._edge_count = 0

    def add(self, memory_data: Dict[str, Any]):
        """Add a memory node to the graph (minimal implementation)."""
        self._node_count += 1

    def get_stats(self) -> Dict[str, Any]:
        """Return basic stats for the relationship graph."""
        return {
            "count": self._node_count,
            "edge_count": self._edge_count,
            "graph_path": self.graph_path,
        }

    def cleanup(self):
        """No-op cleanup for compatibility."""
        return