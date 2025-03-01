import os
import json
import time
from datetime import datetime, timedelta
import hashlib
from typing import Optional, Dict, Any

class CacheManager:
    def __init__(self, cache_dir: str = 'cache', expiration_hours: int = 24):
        """Initialize the cache manager.
        
        Args:
            cache_dir (str): Directory to store cache files
            expiration_hours (int): Number of hours before cache expires
        """
        self.cache_dir = os.path.join(os.path.dirname(__file__), cache_dir)
        self.expiration_hours = expiration_hours
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self) -> None:
        """Create cache directory if it doesn't exist."""
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Create metadata file if it doesn't exist
        metadata_file = os.path.join(self.cache_dir, 'metadata.json')
        if not os.path.exists(metadata_file):
            self._save_metadata({
                'created_at': datetime.now().isoformat(),
                'last_cleanup': datetime.now().isoformat(),
                'total_entries': 0,
                'size_bytes': 0
            })
    
    def _get_cache_path(self, key: str) -> str:
        """Get the file path for a cache key.
        
        Args:
            key (str): Cache key
            
        Returns:
            str: Path to cache file
        """
        # Create a hash of the key to use as filename
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed_key}.json")
    
    def _save_metadata(self, metadata: Dict[str, Any]) -> None:
        """Save cache metadata.
        
        Args:
            metadata (dict): Metadata to save
        """
        metadata_file = os.path.join(self.cache_dir, 'metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata.
        
        Returns:
            dict: Cache metadata
        """
        metadata_file = os.path.join(self.cache_dir, 'metadata.json')
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'created_at': datetime.now().isoformat(),
                'last_cleanup': datetime.now().isoformat(),
                'total_entries': 0,
                'size_bytes': 0
            }
    
    def _update_metadata(self, size_change: int = 0, entries_change: int = 0) -> None:
        """Update cache metadata.
        
        Args:
            size_change (int): Change in cache size in bytes
            entries_change (int): Change in number of entries
        """
        metadata = self._load_metadata()
        metadata['total_entries'] += entries_change
        metadata['size_bytes'] += size_change
        self._save_metadata(metadata)
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from cache.
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[dict]: Cached value if exists and not expired, None otherwise
        """
        cache_path = self._get_cache_path(key)
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            # Check if cache has expired
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cache_time > timedelta(hours=self.expiration_hours):
                self.delete(key)
                return None
                
            return cache_data['data']
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return None
    
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """Set value in cache.
        
        Args:
            key (str): Cache key
            value (dict): Value to cache
        """
        cache_path = self._get_cache_path(key)
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': value,
            'key': key
        }
        
        # Calculate size change
        old_size = os.path.getsize(cache_path) if os.path.exists(cache_path) else 0
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2)
            
        new_size = os.path.getsize(cache_path)
        self._update_metadata(
            size_change=new_size - old_size,
            entries_change=0 if os.path.exists(cache_path) else 1
        )
    
    def delete(self, key: str) -> bool:
        """Delete value from cache.
        
        Args:
            key (str): Cache key
            
        Returns:
            bool: True if value was deleted, False otherwise
        """
        cache_path = self._get_cache_path(key)
        try:
            size = os.path.getsize(cache_path)
            os.remove(cache_path)
            self._update_metadata(size_change=-size, entries_change=-1)
            return True
        except FileNotFoundError:
            return False
    
    def cleanup(self, max_age_hours: Optional[int] = None) -> int:
        """Clean up expired cache entries.
        
        Args:
            max_age_hours (int, optional): Override default expiration time
            
        Returns:
            int: Number of entries cleaned up
        """
        max_age = max_age_hours or self.expiration_hours
        cleaned = 0
        
        for filename in os.listdir(self.cache_dir):
            if filename == 'metadata.json':
                continue
                
            file_path = os.path.join(self.cache_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cache_time > timedelta(hours=max_age):
                    size = os.path.getsize(file_path)
                    os.remove(file_path)
                    self._update_metadata(size_change=-size, entries_change=-1)
                    cleaned += 1
                    
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                continue
        
        # Update last cleanup time
        metadata = self._load_metadata()
        metadata['last_cleanup'] = datetime.now().isoformat()
        self._save_metadata(metadata)
        
        return cleaned
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            dict: Cache statistics
        """
        metadata = self._load_metadata()
        metadata['cache_dir'] = self.cache_dir
        metadata['expiration_hours'] = self.expiration_hours
        return metadata
