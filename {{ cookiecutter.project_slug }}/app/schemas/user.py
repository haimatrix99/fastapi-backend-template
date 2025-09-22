{% if cookiecutter.include_example == "y" %}
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    {% if cookiecutter.include_database == "y" %}
    model_config = ConfigDict(from_attributes=True)
    {% else %}
    class Config:
        orm_mode = True
    {% endif %}
{%- endif %}
