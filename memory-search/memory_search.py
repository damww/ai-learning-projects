#!/usr/bin/env python3
"""
Memory Search Skill - Local semantic search using ChromaDB
"""

import sys
import json
import os
from pathlib import Path

# Try to import chromadb
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

def load_config():
    """Load skill configuration"""
    config_path = Path(__file__).parent / "config.json"
    default_config = {
        "db_path": str(Path(__file__).parent / "memory_db"),
        "collection_name": "memories",
        "embedding_model": "all-MiniLM-L6-v2"
    }
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception as e:
            print(f"Warning: Failed to load config: {e}", file=sys.stderr)
    
    return default_config

def get_chroma_client(config):
    """Initialize ChromaDB client"""
    if not CHROMADB_AVAILABLE:
        raise ImportError("ChromaDB not installed. Run: pip install chromadb")
    
    db_path = config["db_path"]
    
    # Ensure directory exists
    os.makedirs(db_path, exist_ok=True)
    
    # Initialize client with persistence
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=db_path,
        anonymized_telemetry=False
    ))
    
    return client

def get_or_create_collection(client, config):
    """Get or create the memories collection"""
    collection_name = config["collection_name"]
    
    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        # Collection doesn't exist, create it
        collection = client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    return collection

def search_memories(query, n_results=5):
    """Search memories semantically"""
    try:
        config = load_config()
        client = get_chroma_client(config)
        collection = get_or_create_collection(client, config)
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                formatted.append({
                    "id": doc_id,
                    "content": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None
                })
        
        return {"success": True, "results": formatted, "query": query}
        
    except ImportError as e:
        return {"success": False, "error": f"Missing dependency: {str(e)}", "results": []}
    except Exception as e:
        return {"success": False, "error": str(e), "results": []}

def add_memory(text, metadata=None):
    """Add a memory to the collection"""
    try:
        config = load_config()
        client = get_chroma_client(config)
        collection = get_or_create_collection(client, config)
        
        # Generate a simple ID based on timestamp
        import time
        memory_id = f"mem_{int(time.time() * 1000)}"
        
        if metadata is None:
            metadata = {}
        metadata["timestamp"] = time.time()
        
        collection.add(
            ids=[memory_id],
            documents=[text],
            metadatas=[metadata]
        )
        
        return {"success": True, "id": memory_id, "text": text}
        
    except ImportError as e:
        return {"success": False, "error": f"Missing dependency: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_memories(limit=10):
    """List recent memories"""
    try:
        config = load_config()
        client = get_chroma_client(config)
        collection = get_or_create_collection(client, config)
        
        # Get all documents (limited)
        results = collection.get(
            limit=limit,
            include=["documents", "metadatas"]
        )
        
        formatted = []
        if results["ids"]:
            for i, doc_id in enumerate(results["ids"]):
                formatted.append({
                    "id": doc_id,
                    "content": results["documents"][i] if results["documents"] else "",
                    "metadata": results["metadatas"][i] if results["metadatas"] else {}
                })
        
        return {"success": True, "memories": formatted}
        
    except ImportError as e:
        return {"success": False, "error": f"Missing dependency: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """Main entry point for CLI usage"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: memory_search.py <command> [args]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        n_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        result = search_memories(query, n_results)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "add":
        text = sys.argv[2] if len(sys.argv) > 2 else ""
        result = add_memory(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        result = list_memories(limit)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
