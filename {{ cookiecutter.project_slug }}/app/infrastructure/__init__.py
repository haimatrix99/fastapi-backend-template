"""Infrastructure for {{ cookiecutter.project_name }}."""

from .http_client import get_http_client
{% if cookiecutter.include_database == "y" -%}
from .database import Base, get_db, init_db, close_db
{%- endif %}

__all__ = [
    "get_http_client",
{% if cookiecutter.include_database == "y" -%}
    "Base",
    "get_db",
    "init_db",
    "close_db",
{%- endif %}
]