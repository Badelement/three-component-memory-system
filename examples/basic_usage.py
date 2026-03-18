#!/usr/bin/env python3
"""
Basic usage examples for Three-Component Memory System.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from three_component_memory import MemorySystem

def example_1_basic_operations():
    """Example 1: Basic memory operations."""
    print("🧪 Example 1: Basic Memory Operations")
    print("=" * 50)
    
    # Initialize the system
    memory = MemorySystem()
    print("✅ Memory system initialized")
    
    # Add a memory
    memory_id = memory.add(
        content="Project decision: Use microservices architecture for better scalability",
        category="project",
        tags=["architecture", "decision", "important"],
        importance=4
    )
    print(f"✅ Added memory: {memory_id}")
    
    # Search memories
    results = memory.search("microservices architecture", search_type="semantic")
    print(f"✅ Found {len(results)} related memories")
    
    for i, mem in enumerate(results, 1):
        print(f"  {i}. Score: {mem.get('score', 0):.3f}")
        print(f"     Content: {mem.get('content', '')[:60]}...")
    
    # Get system statistics
    stats = memory.get_stats()
    print(f"📊 System status: {stats.get('status', 'unknown')}")
    print(f"📊 Memory count: {stats.get('memory_count', 0)}")
    
    print()

def example_2_auto_recording():
    """Example 2: Automatic conversation recording."""
    print("🧪 Example 2: Automatic Conversation Recording")
    print("=" * 50)
    
    memory = MemorySystem()
    
    # Simulate important conversation (should be recorded)
    important_convo = memory.auto_record(
        user_message="How can we optimize token usage in AI conversations?",
        ai_response="The three-component system can save 70-90% tokens through structured storage and semantic search."
    )
    
    if important_convo:
        print(f"✅ Important conversation recorded: {important_convo}")
    else:
        print("⚠️  Conversation not recorded (may not meet importance threshold)")
    
    # Simulate casual conversation (may not be recorded)
    casual_convo = memory.auto_record(
        user_message="What's the weather like today?",
        ai_response="I don't have weather information, but you can check a weather app."
    )
    
    if casual_convo:
        print(f"✅ Casual conversation recorded: {casual_convo}")
    else:
        print("✅ Casual conversation correctly not recorded")
    
    print()

def example_3_different_search_types():
    """Example 3: Different search types comparison."""
    print("🧪 Example 3: Search Types Comparison")
    print("=" * 50)
    
    memory = MemorySystem()
    
    # Add some test memories
    test_memories = [
        "Using vector databases for semantic search",
        "SQLite provides fast structured storage",
        "NetworkX helps discover relationships between memories",
        "Three-component architecture combines multiple technologies"
    ]
    
    for content in test_memories:
        memory.add(content, category="test", importance=2)
    
    # Test different search types
    query = "database search technology"
    
    for search_type in ["semantic", "text", "hybrid"]:
        results = memory.search(query, search_type=search_type, limit=2)
        print(f"🔍 {search_type.capitalize()} search:")
        print(f"   Found {len(results)} results")
        if results:
            print(f"   Best match: {results[0].get('content', '')[:50]}...")
        print()
    
    print()

def example_4_context_retrieval():
    """Example 4: Context retrieval for conversations."""
    print("🧪 Example 4: Context Retrieval")
    print("=" * 50)
    
    memory = MemorySystem({"debug": False})
    
    # Add some context memories
    context_memories = [
        "We decided to use LanceDB for vector storage",
        "The project timeline is Q2 2026 for MVP launch",
        "Team decided to adopt Agile methodology",
        "Technical stack: Python, LanceDB, SQLite, NetworkX"
    ]
    
    for content in context_memories:
        memory.add(content, category="project", importance=3)
    
    # Get context for current conversation
    current_topic = "discussing our technical architecture choices"
    context = memory.get_context(current_topic, limit=2)
    
    print(f"Current topic: {current_topic}")
    print(f"Retrieved {len(context)} relevant context memories:")
    
    for i, item in enumerate(context, 1):
        print(f"  {i}. Relevance: {item.get('score', 0):.3f}")
        print(f"     {item.get('content', '')[:60]}...")
    
    print()

def main():
    """Run all examples."""
    print("🚀 Three-Component Memory System - Examples")
    print("=" * 60)
    print()
    
    example_1_basic_operations()
    example_2_auto_recording()
    example_3_different_search_types()
    example_4_context_retrieval()
    
    print("🎉 All examples completed!")
    print()
    print("💡 Next steps:")
    print("1. Check the docs/ directory for detailed documentation")
    print("2. Read the API reference for all available methods")
    print("3. Try integrating with your own OpenClaw setup")

if __name__ == "__main__":
    main()
