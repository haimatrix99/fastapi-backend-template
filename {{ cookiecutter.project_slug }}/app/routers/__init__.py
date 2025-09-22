from .health import health_router
{% if cookiecutter.include_example == "y" -%}
from .users import users_router
{%- endif %}

__all__ = [
    "health_router",
    {% if cookiecutter.include_example == "y" -%}
    "users_router",
    {%- endif %}
]