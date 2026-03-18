# Three-Component Memory System - Examples

## Basic Examples

### Example 1: Simple Memory Management
```python
from three_component_memory import MemorySystem

# Initialize
memory = MemorySystem()

# Add a memory
memory_id = memory.add(
    content="Learned about three-component architecture today",
    category="learning",
    tags=["architecture", "knowledge"],
    importance=3
)

print(f"Added memory: {memory_id}")

# Search for it
results = memory.search("three component architecture")
for mem in results:
    print(f"Found: {mem.content[:50]}...")
```

### Example 2: Project Decision Logging
```python
# Log project decisions
decisions = [
    {
        "content": "Decision: Use React for frontend, Node.js for backend",
        "category": "project",
        "tags": ["technology", "decision", "architecture"],
        "importance": 4
    },
    {
        "content": "Team decided to adopt Agile methodology",
        "category": "process", 
        "tags": ["methodology", "team", "decision"],
        "importance": 3
    },
    {
        "content": "Choose AWS as cloud provider for scalability",
        "category": "infrastructure",
        "tags": ["cloud", "aws", "decision"],
        "importance": 5
    }
]

for decision in decisions:
    memory.add(**decision)
    print(f"Logged decision: {decision['content'][:30]}...")
```

### Example 3: Learning Progress Tracking
```python
# Track learning progress
learning_topics = [
    "Understanding vector databases and LanceDB",
    "Learning about semantic search algorithms", 
    "Exploring graph databases with NetworkX",
    "Studying token optimization techniques"
]

for topic in learning_topics:
    memory.add(
        content=f"Studied: {topic}",
        category="learning",
        tags=["study", "progress"],
        importance=2
    )

# Later, review what you've learned
review = memory.search("what have I learned about databases")
print(f"Found {len(review)} related learning memories")
```

## Advanced Examples

### Example 4: Meeting Notes Management
```python
class MeetingNotesManager:
    def __init__(self):
        self.memory = MemorySystem()
    
    def record_meeting(self, title, date, participants, notes, decisions):
        """Record meeting notes and decisions"""
        # Record meeting summary
        summary = f"Meeting: {title} on {date}\nParticipants: {participants}\nNotes: {notes}"
        
        memory_id = self.memory.add(
            content=summary,
            category="meeting",
            tags=["meeting", title.replace(" ", "-").lower(), date],
            importance=4,
            metadata={
                "title": title,
                "date": date,
                "participants": participants,
                "note_count": len(notes.split("\n"))
            }
        )
        
        # Record individual decisions
        for decision in decisions:
            self.memory.add(
                content=f"Decision from {title}: {decision}",
                category="decision",
                tags=["meeting-decision", title.replace(" ", "-").lower()],
                importance=5
            )
        
        return memory_id
    
    def find_meeting_decisions(self, project_name):
        """Find all decisions related to a project"""
        return self.memory.search(
            f"decisions about {project_name}",
            search_type="hybrid"
        )

# Usage
manager = MeetingNotesManager()
meeting_id = manager.record_meeting(
    title="Q4 Planning",
    date="2026-03-18",
    participants=["Alice", "Bob", "Charlie"],
    notes="Discussed project timelines and resource allocation",
    decisions=[
        "Launch MVP by end of April",
        "Hire two more developers",
        "Increase marketing budget by 20%"
    ]
)

# Find decisions later
decisions = manager.find_meeting_decisions("Q4")
```

### Example 5: Personal Knowledge Base
```python
class PersonalKnowledgeBase:
    def __init__(self):
        self.memory = MemorySystem({
            "auto_record": True,
            "importance_threshold": 2  # Record more things
        })
    
    def add_insight(self, insight, topic, source=None):
        """Add a personal insight or learning"""
        tags = ["insight", "knowledge"]
        if source:
            tags.append(source.lower().replace(" ", "-"))
        
        return self.memory.add(
            content=insight,
            category="insight",
            tags=tags,
            importance=3,
            metadata={"source": source, "topic": topic}
        )
    
    def connect_insights(self, insight_id_1, insight_id_2, relationship):
        """Connect two insights"""
        # This would use the relationship graph
        pass
    
    def explore_topic(self, topic):
        """Explore everything known about a topic"""
        # Semantic search for the topic
        direct = self.memory.search(topic, search_type="semantic")
        
        # Text search for exact matches
        exact = self.memory.search(topic, search_type="text")
        
        # Combine and deduplicate
        all_insights = {}
        for insight in direct + exact:
            all_insights[insight.id] = insight
        
        return list(all_insights.values())

# Usage
kb = PersonalKnowledgeBase()

# Add insights
kb.add_insight(
    "Vector databases are great for semantic search",
    topic="databases",
    source="Personal experience"
)

kb.add_insight(
    "LanceDB provides good performance for local vector storage",
    topic="databases", 
    source="Documentation"
)

# Explore a topic
database_insights = kb.explore_topic("databases")
print(f"Found {len(database_insights)} insights about databases")
```

### Example 6: Code Snippet Library
```python
class CodeSnippetLibrary:
    def __init__(self):
        self.memory = MemorySystem()
    
    def add_snippet(self, code, language, description, tags):
        """Add a code snippet"""
        content = f"""Language: {language}
Description: {description}

Code:
{code}"""
        
        return self.memory.add(
            content=content,
            category="code",
            tags=["code", language.lower()] + tags,
            importance=3,
            metadata={
                "language": language,
                "line_count": len(code.split("\n")),
                "has_comments": "#" in code or "//" in code
            }
        )
    
    def find_snippet(self, description, language=None):
        """Find code snippets by description"""
        query = description
        if language:
            query = f"{description} {language}"
        
        return self.memory.search(query, search_type="hybrid")
    
    def get_snippets_by_language(self, language):
        """Get all snippets for a language"""
        return self.memory.search(
            language,
            search_type="text"  # Text search for exact language match
        )

# Usage
library = CodeSnippetLibrary()

# Add Python snippet
library.add_snippet(
    code="""def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""",
    language="Python",
    description="Fibonacci sequence recursive implementation",
    tags=["algorithm", "recursion", "math"]
)

# Add JavaScript snippet  
library.add_snippet(
    code="""function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}""",
    language="JavaScript",
    description="Debounce function for performance optimization",
    tags=["performance", "utility", "function"]
)

# Find snippets
python_snippets = library.find_snippet("recursive function", "Python")
print(f"Found {len(python_snippets)} Python recursive functions")
```

## Integration Examples

### Example 7: OpenClaw Integration
```python
# This is how OpenClaw integrates with the memory system
class OpenClawMemoryIntegration:
    def __init__(self):
        self.memory = MemorySystem()
    
    def process_conversation(self, user_message, ai_response):
        """Process a conversation turn"""
        # Auto-record if important
        memory_id = self.memory.auto_record(user_message, ai_response)
        
        # Get relevant context for next response
        context = self.memory.get_context(user_message)
        
        return {
            "recorded": memory_id is not None,
            "context": context,
            "memory_id": memory_id
        }
    
    def handle_command(self, command, args):
        """Handle memory-related commands"""
        if command == "search":
            return self.memory.search(args[0], limit=5)
        elif command == "stats":
            return self.memory.get_stats()
        elif command == "config":
            if len(args) >= 2:
                # Update configuration
                self.memory.update_config({args[0]: args[1]})
                return {"success": True, "message": "Configuration updated"}
        return {"error": "Unknown command"}
```

### Example 8: Web Application Integration
```python
from flask import Flask, request, jsonify

app = Flask(__name__)
memory = MemorySystem()

@app.route('/api/memories', methods=['POST'])
def add_memory():
    data = request.json
    memory_id = memory.add(
        content=data['content'],
        category=data.get('category', 'general'),
        tags=data.get('tags', []),
        importance=data.get('importance', 3)
    )
    return jsonify({"id": memory_id})

@app.route('/api/memories/search', methods=['GET'])
def search_memories():
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'hybrid')
    limit = int(request.args.get('limit', 5))
    
    results = memory.search(query, search_type=search_type, limit=limit)
    
    # Convert to JSON-serializable format
    serialized = []
    for mem in results:
        serialized.append({
            "id": mem.id,
            "content": mem.content,
            "category": mem.category,
            "tags": mem.tags,
            "importance": mem.importance,
            "score": mem.score
        })
    
    return jsonify({"results": serialized})

@app.route('/api/memories/stats', methods=['GET'])
def get_stats():
    return jsonify(memory.get_stats())
```

## Performance Examples

### Example 9: Benchmarking
```python
import time

def benchmark_search(memory, query, iterations=100):
    """Benchmark search performance"""
    times = []
    
    for i in range(iterations):
        start = time.time()
        results = memory.search(query)
        end = time.time()
        times.append((end - start) * 1000)  # Convert to ms
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    return {
        "iterations": iterations,
        "avg_time_ms": avg_time,
        "min_time_ms": min_time,
        "max_time_ms": max_time,
        "query": query
    }

# Run benchmarks
memory = MemorySystem()
benchmarks = [
    benchmark_search(memory, "test query", 50),
    benchmark_search(memory, "longer test query for semantic search", 50),
    benchmark_search(memory, "三组件系统", 50)
]

for bench in benchmarks:
    print(f"Query: {bench['query']}")
    print(f"  Average: {bench['avg_time_ms']:.2f}ms")
    print(f"  Range: {bench['min_time_ms']:.2f}-{bench['max_time_ms']:.2f}ms")
```

### Example 10: Bulk Operations
```python
def import_large_dataset(memory, dataset_path):
    """Import a large dataset efficiently"""
    import json
    
    with open(dataset_path, 'r') as f:
        data = json.load(f)
    
    batch_size = 100
    total = len(data)
    imported = 0
    
    for i in range(0, total, batch_size):
        batch = data[i:i+batch_size]
        
        for item in batch:
            memory.add(
                content=item['content'],
                category=item.get('category', 'general'),
                tags=item.get('tags', []),
                importance=item.get('importance', 3)
            )
        
        imported += len(batch)
        print(f"Imported {imported}/{total} items")
    
    return imported

# Usage
# count = import_large_dataset(memory, "large_dataset.json")
# print(f"Imported {count} items total")
```

---

**Examples Version**: 1.0.0  
**Last Updated**: 2026-03-18
