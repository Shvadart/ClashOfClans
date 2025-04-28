#cache.py
import json
import os
from datetime import datetime

CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache.json")

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cache(data):
    data["last_update"] = datetime.now().isoformat()
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_cached_townhall():
    cache = load_cache()
    return cache.get("townhall_level")

def set_townhall(level):
    cache = load_cache()
    cache["townhall_level"] = level
    save_cache(cache)

def get_cached_storage(resource_type):
    cache = load_cache()
    return cache.get("storage_levels", {}).get(resource_type, {})

def update_storage_level(resource_type, level):
    cache = load_cache()
    if "storage_levels" not in cache:
        cache["storage_levels"] = {}
    if resource_type not in cache["storage_levels"]:
        cache["storage_levels"][resource_type] = {}

    count = cache["storage_levels"][resource_type].get(str(level), 0)
    cache["storage_levels"][resource_type][str(level)] = count + 1
    save_cache(cache)
