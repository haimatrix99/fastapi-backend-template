{% if cookiecutter.include_example == "y" -%}
from .user import User

__all__ = ["User"]
{% else -%}
__all__ = []
{%- endif %}