#!/usr/bin/env python3
"""
Simple Memory Skill - Lightweight memory storage with keyword search
No external dependencies - uses only Python standard library
"""

import sys
import json
import re
import os
from datetime import datetime
from pathlib import Path

# Get the skill directory
SKILL_DIR = Path(__file__).parent
MEMORY_FILE = SKILL_DIR / "memory.json"

def load_memories():
    """Load all memories from file"""
    if not MEMORY_FILE.exists():
        return []
    
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading memories: {e}", file=sys.stderr)
        return []

def save_memories(memories):
    """Save all memories to file"""
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(memories, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving memories: {e}", file=sys.stderr)
        return False

def search_memories(query, limit=10):
    """Search memories by keyword (simple text matching)"""
    memories = load_memories()
    
    if not query or not query.strip():
        # Return most recent memories if no query
        sorted_memories = sorted(
            memories, 
            key=lambda x: x.get('timestamp', ''), 
            reverse=True
        )
        return sorted_memories[:limit]
    
    query_lower = query.lower()
    query_words = query_lower.split()
    
    # Score each memory based on match quality
    scored_memories = []
    
    for memory in memories:
        content = memory.get('content', '').lower()
        tags = memory.get('tags', [])
        
        score = 0
        
        # Full phrase match gets highest score
        if query_lower in content:
            score += 10
        
        # Individual word matches
        for word in query_words:
            if word in content:
                score += 3
        
        # Tag matches
        for tag in tags:
            if query_lower in tag.lower():
                score += 5
        
        if score > 0:
            scored_memories.append((score, memory))
    
    # Sort by score descending, then by timestamp
    scored_memories.sort(
        key=lambda x: (-x[0], x[1].get('timestamp', '')),
        reverse=True
    )
    
    # Return top results
    return [m for _, m in scored_memories[:limit]]

def add_memory(content, tags=None):
    """Add a new memory"""
    if not content or not content.strip():
        return {"success": False, "error": "Content cannot be empty"}
    
    memories = load_memories()
    
    # Generate a unique ID
    memory_id = f"mem_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(memories)}"
    
    new_memory = {
        "id": memory_id,
        "content": content.strip(),
        "timestamp": datetime.now().isoformat(),
        "tags": tags or []
    }
    
    memories.append(new_memory)
    
    if save_memories(memories):
        return {"success": True, "memory": new_memory}
    else:
        return {"success": False, "error": "Failed to save memory"}

def delete_memory(memory_id):
    """Delete a memory by ID"""
    memories = load_memories()
    
    original_count = len(memories)
    memories = [m for m in memories if m.get("id") != memory_id]
    
    if len(memories) == original_count:
        return {"success": False, "error": "Memory not found"}
    
    if save_memories(memories):
        return {"success": True, "deleted_id": memory_id}
    else:
        return {"success": False, "error": "Failed to save after deletion"}

def clear_all_memories():
    """Clear all memories"""
    try:
        if MEMORY_FILE.exists():
            MEMORY_FILE.unlink()
        return {"success": True, "message": "All memories cleared"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: memory.py <command> [args]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        results = search_memories(query, limit)
        print(json.dumps({"success": True, "results": results}, indent=2, ensure_ascii=False))
    
    elif command == "add":
        text = sys.argv[2] if len(sys.argv) > 2 else ""
        result = add_memory(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "delete":
        memory_id = sys.argv[2] if len(sys.argv) > 2 else ""
        result = delete_memory(memory_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        results = search_memories("", limit)
        print(json.dumps({"success": True, "results": results}, indent=2, ensure_ascii=False))
    
    elif command == "clear":
        result = clear_all_memories()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
