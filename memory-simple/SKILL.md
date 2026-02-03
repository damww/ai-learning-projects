# Simple Memory Skill

A lightweight memory skill using simple text search (no external dependencies).

## Description

This skill provides basic memory storage and keyword search functionality without requiring ChromaDB or vector databases. It uses simple text matching and works out of the box.

## Usage

### Search Memories

```
/memory <query>
```

Examples:
```
/memory OpenClaw
/memory 项目配置
```

### Add Memory

```
/memory-add <text>
```

Examples:
```
/memory-add 用户偏好使用深色模式
/memory-add Project X deadline is March 15
```

### List Memories

```
/memory-list [limit]
```

### Clear All Memories

```
/memory-clear
```

## Storage

Memories are stored in `memory.json` file in the skill directory. The file is plain JSON and human-readable.

## Limitations

- Uses simple keyword matching (not semantic search)
- No vector embeddings
- Best for small to medium memory sets
- Search is case-insensitive but not fuzzy

## Dependencies

- Python 3.8+ (standard library only - no external packages!)
