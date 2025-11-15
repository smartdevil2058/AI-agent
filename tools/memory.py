import os
import json
from typing import List, Dict

MEM_FILE = 'memory_store.json'
os.makedirs(os.path.dirname(MEM_FILE) or '.', exist_ok=True)

def _load() -> List[Dict]:
    if not os.path.exists(MEM_FILE):
        return []
    try:
        return json.load(open(MEM_FILE, 'r', encoding='utf-8'))
    except Exception:
        return []

def add_memory(key: str, value):
    mem = _load()
    mem.append({'key': key, 'value': value})
    with open(MEM_FILE, 'w', encoding='utf-8') as f:
        json.dump(mem, f, indent=2, ensure_ascii=False)

def search_memory(query: str, top_k: int = 3):
    # Toy retrieval: return last matching top_k entries whose key or value text contains tokens from query.
    mem = _load()[::-1]  # reverse for recency
    results = []
    q = query.lower()
    for item in mem:
        if q in str(item.get('key','')).lower() or q in str(item.get('value','')).lower():
            results.append(item)
            if len(results) >= top_k:
                break
    return results
