{% if cookiecutter.include_example == "y" -%}
from typing import Optional

from fastapi import APIRouter, status, HTTPException

from app.utils.cache import CacheManager

cache_router = APIRouter(prefix="/cache", tags=["Cache"])


@cache_router.get("/get/{key}")
async def get_cache(key: str):
    """Get value from cache by key."""
    value = await CacheManager.get(key)
    if value is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Key '{key}' not found in cache"
        )
    return {"key": key, "value": value}


@cache_router.post("/set/{key}")
async def set_cache(key: str, value: str, ttl: Optional[int] = None):
    """Set value in cache with optional TTL (in seconds)."""
    success = await CacheManager.set(key, value, ttl)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set cache value"
        )
    return {"key": key, "value": value, "ttl": ttl, "status": "cached"}


@cache_router.delete("/delete/{key}")
async def delete_cache(key: str):
    """Delete key from cache."""
    success = await CacheManager.delete(key)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Key '{key}' not found in cache"
        )
    return {"key": key, "status": "deleted"}


@cache_router.get("/exists/{key}")
async def check_cache(key: str):
    """Check if key exists in cache."""
    exists = await CacheManager.exists(key)
    return {"key": key, "exists": exists}


@cache_router.delete("/clear/{pattern}")
async def clear_cache_pattern(pattern: str):
    """Clear all cache keys matching pattern."""
    deleted_count = await CacheManager.delete_pattern(pattern)
    return {"pattern": pattern, "deleted_count": deleted_count}
{%- endif %}
