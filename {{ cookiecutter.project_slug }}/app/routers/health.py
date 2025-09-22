from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

health_router = APIRouter(tags=["Health"])


@health_router.get("/")
@health_router.get("/health")
async def health():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "healthy"})