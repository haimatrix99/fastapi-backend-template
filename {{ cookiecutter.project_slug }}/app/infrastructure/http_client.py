from typing import Annotated

import httpx
from fastapi import Depends, Request

from app.core import get_settings

settings = get_settings()


async def get_http_client(request: Request) -> httpx.AsyncClient:
    """Get the HTTP client from the app state."""
    return request.app.state.http_client


HttpClient = Annotated[httpx.AsyncClient, Depends(get_http_client)]
