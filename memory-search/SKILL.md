# Memory Search Skill

A skill for semantic memory search using local vector database.

## Description

This skill provides semantic search over your notes and memories using ChromaDB (local vector database). No external API keys required!

## Usage

### Search Memories

```
/memory-search <query>
```

Examples:
```
/memory-search 上次提到的那个项目
/memory-search 用户的偏好设置
```

### Add to Memory

```
/memory-add <text>
```

Adds text to the searchable memory store.

### List Recent Memories

```
/memory-list [limit]
```

Lists recent memory entries.

## Configuration

### 1. Install ChromaDB

```bash
pip install chromadb sentence-transformers
```

### 2. Configure the skill

Edit `skills/memory-search/config.json`:

```json
{
  "db_path": "./memory_db",
  "collection_name": "memories",
  "embedding_model": "all-MiniLM-L6-v2"
}
```

## Dependencies

- Python 3.8+
- chromadb
- sentence-transformers
- numpy

## Notes

- Uses local embedding model (all-MiniLM-L6-v2) - no API calls needed
- Data is stored locally in the configured `db_path`
- First run will download the embedding model (~80MB)
- Suitable for personal use with moderate memory size
