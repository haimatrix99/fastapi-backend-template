{% if cookiecutter.include_example == "y" -%}
from .user import UserBase, UserCreate, UserUpdate, UserResponse

__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserResponse"]
{% else -%}
__all__ = []
{%- endif %}