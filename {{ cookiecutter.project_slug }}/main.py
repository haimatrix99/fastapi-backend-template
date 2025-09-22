from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import get_settings
{% if cookiecutter.include_database == "y" -%}
from app.infrastructure.database import init_db, close_db
{%- endif %}
from app.routers.health import health_router
{% if cookiecutter.include_example == "y" -%}
from app.routers.users import users_router
{%- endif %}

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient()
{% if cookiecutter.include_database == "y" %}
    # Initialize database
    await init_db()
{%- endif %}

    try:
        yield
    finally:
        await app.state.http_client.aclose()
{% if cookiecutter.include_database == "y" %}
        # Close database connections
        await close_db()
{%- endif %}


app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.project_description }}",
    version="{{ cookiecutter.version }}",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
{% if cookiecutter.include_example == "y" -%}
app.include_router(users_router)
{%- endif %}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level,
    )