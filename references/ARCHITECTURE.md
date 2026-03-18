# Three-Component Memory System - Architecture

## System Architecture

### Three-Component Design
```
User Conversation → Three-Component System → Intelligent Response
                        ↓
        LanceDB (Semantic) + SQLite (Structured) + NetworkX (Relationships)
```

### Component Details

#### 1. LanceDB Component (Semantic Layer)
- **Purpose**: Vector-based semantic search
- **Model**: all-MiniLM-L6-v2 (384-dimensional embeddings)
- **Storage**: Vector database for similarity search
- **Performance**: 5-15ms per query

#### 2. SQLite Component (Structured Layer)
- **Purpose**: Metadata management and fast queries
- **Schema**: 
  - memories (id, content, category, tags, importance, created_at)
  - relationships (source_id, target_id, relationship_type, strength)
- **Indexes**: Full-text search on content, indexes on category/tags
- **Performance**: 1-5ms per query

#### 3. NetworkX Component (Relationship Layer)
- **Purpose**: Discover and maintain memory relationships
- **Graph Structure**: 
  - Nodes: Memories
  - Edges: Relationships (semantic, temporal, categorical)
- **Algorithms**: Community detection, shortest path, centrality
- **Performance**: 2-10ms per traversal

### Data Flow

#### Recording Flow
1. **Input**: User conversation
2. **Analysis**: Importance scoring (length, keywords, context)
3. **Processing**: 
   - Text → Vector embedding (LanceDB)
   - Metadata extraction (SQLite)
   - Relationship analysis (NetworkX)
4. **Storage**: Parallel write to three components
5. **Verification**: Consistency check across components

#### Search Flow
1. **Query**: User search request
2. **Parallel Search**:
   - Semantic: LanceDB vector similarity
   - Text: SQLite full-text search
   - Relationship: NetworkX graph traversal
3. **Result Fusion**: Weighted combination of results
4. **Ranking**: Relevance scoring and sorting
5. **Output**: Ranked list of memories

### Consistency Model

#### Eventual Consistency
- **Write**: Atomic across three components
- **Read**: Strong consistency for single component, eventual for cross-component
- **Recovery**: Automatic consistency repair on startup

#### Data Synchronization
- **Primary**: SQLite as source of truth
- **Secondary**: LanceDB and NetworkX synchronized from SQLite
- **Conflict Resolution**: Timestamp-based, last-write-wins

### Performance Characteristics

#### Storage Efficiency
- **Text Compression**: 60-80% reduction through structured storage
- **Vector Storage**: 384-dimensional floats (1.5KB per memory)
- **Graph Storage**: Adjacency lists with compression

#### Query Performance
- **Simple Query**: <10ms (95th percentile)
- **Complex Query**: <50ms (95th percentile)
- **Bulk Operations**: Linear scaling with batch size

#### Memory Usage
- **Working Set**: 50-200MB for 10,000 memories
- **Cache**: LRU cache for frequent queries
- **Growth**: Linear with memory count

### Scalability Considerations

#### Vertical Scaling
- **Memory**: 1GB per 100,000 memories
- **CPU**: Single-core bound, parallelizable queries
- **Disk**: 10MB per 1,000 memories

#### Horizontal Scaling (Future)
- **Sharding**: By user ID or time range
- **Replication**: Read replicas for high availability
- **Partitioning**: Separate components on different nodes

### Security Model

#### Data Protection
- **Encryption**: At-rest encryption for sensitive data
- **Access Control**: User-based permission model
- **Audit Logging**: All operations logged with timestamps

#### Privacy Features
- **Local Storage**: All data stays on user device
- **No Telemetry**: No data sent to external servers
- **User Control**: Full export/import capabilities

### Monitoring and Maintenance

#### Health Checks
- **Component Status**: Each component heartbeat
- **Data Consistency**: Periodic cross-component verification
- **Performance Metrics**: Query latency, memory usage, disk space

#### Maintenance Operations
- **Backup**: Full and incremental backups
- **Compaction**: Periodic database optimization
- **Cleanup**: Automatic removal of old/unimportant memories

### Integration Points

#### OpenClaw Integration
- **Skill Interface**: Standard OpenClaw skill API
- **Event Handling**: Conversation events and commands
- **Configuration**: OpenClaw config.json integration

#### External APIs (Future)
- **Export Formats**: JSON, CSV, Markdown
- **Import Sources**: Existing memory systems
- **Sync Services**: Cloud backup (optional)
