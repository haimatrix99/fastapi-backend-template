import json
from functools import wraps
from typing import Any, Callable, Optional

from app.infrastructure.redis import get_redis


class CacheManager:
    """Helper class for managing cache operations."""
    
    @staticmethod
    async def get(key: str) -> Optional[str]:
        """Get value from cache."""
        redis = await get_redis()
        if redis is None:
            return None
        
        try:
            return await redis.get(key)
        except Exception:
            return None
    
    @staticmethod
    async def set(key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL (in seconds)."""
        redis = await get_redis()
        if redis is None:
            return False
        
        try:
            if ttl:
                await redis.setex(key, ttl, value)
            else:
                await redis.set(key, value)
            return True
        except Exception:
            return False
    
    @staticmethod
    async def delete(key: str) -> bool:
        """Delete key from cache."""
        redis = await get_redis()
        if redis is None:
            return False
        
        try:
            await redis.delete(key)
            return True
        except Exception:
            return False
    
    @staticmethod
    async def delete_pattern(pattern: str) -> int:
        """Delete all keys matching pattern."""
        redis = await get_redis()
        if redis is None:
            return 0
        
        try:
            keys = await redis.keys(pattern)
            if keys:
                return await redis.delete(*keys)
            return 0
        except Exception:
            return 0
    
    @staticmethod
    async def exists(key: str) -> bool:
        """Check if key exists in cache."""
        redis = await get_redis()
        if redis is None:
            return False
        
        try:
            return await redis.exists(key) > 0
        except Exception:
            return False
    
    @staticmethod
    async def get_json(key: str) -> Optional[Any]:
        """Get JSON value from cache."""
        value = await CacheManager.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return None
    
    @staticmethod
    async def set_json(key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set JSON value in cache with optional TTL (in seconds)."""
        try:
            json_value = json.dumps(value)
            return await CacheManager.set(key, json_value, ttl)
        except (TypeError, ValueError):
            return False


def cache_result(key_prefix: str, ttl: Optional[int] = None):
    """
    Decorator to cache function results.
    
    Args:
        key_prefix: Prefix for the cache key
        ttl: Time to live in seconds (optional)
    
    Example:
        @cache_result("user", ttl=300)
        async def get_user(user_id: int):
            # Function implementation
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function arguments
            cache_key = f"{key_prefix}:{args}:{kwargs}"
            
            # Try to get from cache
            cached_value = await CacheManager.get_json(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            if result is not None:
                await CacheManager.set_json(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


def invalidate_cache(key_pattern: str):
    """
    Decorator to invalidate cache after function execution.
    
    Args:
        key_pattern: Pattern of cache keys to invalidate
    
    Example:
        @invalidate_cache("user:*")
        async def update_user(user_id: int, data: dict):
            # Function implementation
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            await CacheManager.delete_pattern(key_pattern)
            return result
        
        return wrapper
    return decorator
