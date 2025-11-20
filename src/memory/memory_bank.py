"""
Simple memory bank for storing user profiles and progress
"""
from typing import Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path


class MemoryBank:
    """Simple in-memory storage for user data"""
    
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or Path("data/user_memory")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def store(self, namespace: str, key: str, value: Any, user_id: Optional[str] = None):
        """Store data in memory bank"""
        namespace_dir = self.storage_dir / namespace
        namespace_dir.mkdir(exist_ok=True)
        
        entry = {
            "key": key,
            "value": value,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        file_path = namespace_dir / f"{key}.json"
        with open(file_path, 'w') as f:
            json.dump(entry, f, indent=2)
        
        cache_key = f"{namespace}:{key}"
        self.cache[cache_key] = entry
    
    def retrieve(self, namespace: str, key: str) -> Optional[Any]:
        """Retrieve data from memory bank"""
        cache_key = f"{namespace}:{key}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]["value"]
        
        file_path = self.storage_dir / namespace / f"{key}.json"
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r') as f:
                entry = json.load(f)
            self.cache[cache_key] = entry
            return entry["value"]
        except:
            return None
    
    def update(self, namespace: str, key: str, updates: Dict[str, Any]):
        """Update existing entry"""
        current_value = self.retrieve(namespace, key)
        
        if current_value is None:
            raise ValueError(f"Entry not found: {namespace}:{key}")
        
        if isinstance(current_value, dict):
            current_value.update(updates)
            updated_value = current_value
        else:
            updated_value = updates.get("value", current_value)
        
        self.store(namespace, key, updated_value)
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile"""
        return self.retrieve("user_profile", user_id)
    
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]):
        """Update user profile"""
        profile = self.get_user_profile(user_id)
        
        if profile is None:
            self.store("user_profile", user_id, updates, user_id=user_id)
        else:
            self.update("user_profile", user_id, updates)
