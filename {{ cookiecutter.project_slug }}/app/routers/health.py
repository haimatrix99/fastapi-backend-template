from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.infrastructure.redis import get_redis

health_router = APIRouter(tags=["Health"])


@health_router.get("/")
@health_router.get("/health")
async def health():
    health_status = {"status": "healthy", "services": {}}
    
    # Check Redis connection
    redis = await get_redis()
    if redis:
        try:
            await redis.ping()
            health_status["services"]["redis"] = "healthy"
        except Exception:
            health_status["services"]["redis"] = "unhealthy"
            health_status["status"] = "degraded"
    else:
        health_status["services"]["redis"] = "disabled"
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=health_status)