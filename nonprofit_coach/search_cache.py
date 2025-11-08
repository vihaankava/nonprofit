"""
Search cache implementation with TTL-based expiration.

This module provides in-memory caching for search results to reduce
API calls, improve performance, and prevent rate limit issues.
"""

import hashlib
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class CacheEntry:
    """Cache entry with data and expiration timestamp."""
    data: Any
    timestamp: datetime
    expires_at: datetime


class SearchCache:
    """
    In-memory cache for search results with TTL-based expiration.
    
    This cache stores search results temporarily to reduce API calls
    and improve response times. Entries automatically expire after
    the configured TTL period.
    """
    
    def __init__(self, ttl_seconds: int = 86400, max_size: int = 1000):
        """
        Initialize the search cache.
        
        Args:
            ttl_seconds: Time-to-live in seconds (default: 24 hours)
            max_size: Maximum number of cache entries (default: 1000)
        """
        self.cache: Dict[str, CacheEntry] = {}
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
    
    def get(self, cache_key: str) -> Optional[Any]:
        """
        Retrieve cached results if not expired.
        
        Args:
            cache_key: The cache key to lookup
            
        Returns:
            Cached data if found and not expired, None otherwise
        """
        if cache_key not in self.cache:
            return None
        
        entry = self.cache[cache_key]
        
        # Check if entry has expired
        if datetime.now() > entry.expires_at:
            # Remove expired entry
            del self.cache[cache_key]
            return None
        
        return entry.data
    
    def set(self, cache_key: str, results: Any):
        """
        Store results in cache with timestamp.
        
        Args:
            cache_key: The cache key to store under
            results: The data to cache
        """
        # Enforce max size by removing oldest entries
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        now = datetime.now()
        expires_at = now + timedelta(seconds=self.ttl_seconds)
        
        entry = CacheEntry(
            data=results,
            timestamp=now,
            expires_at=expires_at
        )
        
        self.cache[cache_key] = entry
    
    def generate_key(self, query: str, params: Dict) -> str:
        """
        Generate a cache key from query and parameters.
        
        Creates a deterministic hash from the query string and
        parameters to ensure consistent cache lookups.
        
        Args:
            query: The search query string
            params: Dictionary of search parameters
            
        Returns:
            SHA256 hash string to use as cache key
        """
        # Create a deterministic string representation
        params_str = json.dumps(params, sort_keys=True)
        key_string = f"{query}:{params_str}"
        
        # Generate hash
        hash_object = hashlib.sha256(key_string.encode())
        return hash_object.hexdigest()
    
    def cleanup_expired(self):
        """
        Remove all expired cache entries.
        
        This method can be called periodically to free memory
        from expired entries that haven't been accessed.
        """
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now > entry.expires_at
        ]
        
        for key in expired_keys:
            del self.cache[key]
    
    def _evict_oldest(self):
        """
        Evict the oldest cache entry to make room for new entries.
        
        Uses LRU-like eviction by removing the entry with the
        oldest timestamp.
        """
        if not self.cache:
            return
        
        # Find the oldest entry
        oldest_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k].timestamp
        )
        
        del self.cache[oldest_key]
    
    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()
    
    def size(self) -> int:
        """
        Get the current number of cache entries.
        
        Returns:
            Number of entries currently in cache
        """
        return len(self.cache)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics including size,
            oldest entry age, and configuration
        """
        stats = {
            'size': len(self.cache),
            'max_size': self.max_size,
            'ttl_seconds': self.ttl_seconds
        }
        
        if self.cache:
            now = datetime.now()
            oldest_entry = min(
                self.cache.values(),
                key=lambda e: e.timestamp
            )
            stats['oldest_entry_age_seconds'] = (
                now - oldest_entry.timestamp
            ).total_seconds()
        
        return stats
