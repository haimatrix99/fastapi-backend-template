from typing import Optional

import redis.asyncio as redis

from app.core import get_settings

settings = get_settings()

# Global Redis connection pool
redis_client: Optional[redis.Redis] = None


async def init_redis() -> None:
    """Initialize Redis connection pool."""
    global redis_client
    
    if not settings.redis_enabled:
        return
    
    redis_client = redis.from_url(
        settings.redis_url,
        max_connections=settings.redis_max_connections,
        decode_responses=settings.redis_decode_responses,
        socket_timeout=settings.redis_socket_timeout,
        socket_connect_timeout=settings.redis_socket_connect_timeout,
    )


async def close_redis() -> None:
    """Close Redis connection pool."""
    global redis_client
    
    if redis_client:
        await redis_client.aclose()
        redis_client = None


async def get_redis() -> Optional[redis.Redis]:
    """Get Redis client instance."""
    return redis_client
