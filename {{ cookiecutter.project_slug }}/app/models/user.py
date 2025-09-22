{% if cookiecutter.include_example == "y" -%}
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

{% if cookiecutter.include_database == "y" -%}
from app.infrastructure.database import Base
{%- endif %}


{% if cookiecutter.include_database == "y" -%}
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
{% else -%}
class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
{%- endif %}
{%- endif %}
