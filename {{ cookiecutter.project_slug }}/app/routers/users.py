{% if cookiecutter.include_example == "y" -%}
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
{% if cookiecutter.include_database == "y" -%}
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_db
{%- endif %}

from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/", response_model=List[UserResponse])
async def get_users({% if cookiecutter.include_database == "y" %}db: AsyncSession = Depends(get_db){% endif %}):
    """Get all users"""
    return await UserService.get_all_users({% if cookiecutter.include_database == "y" %}db{% endif %})


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int{% if cookiecutter.include_database == "y" %}, db: AsyncSession = Depends(get_db){% endif %}):
    """Get a specific user by ID"""
    user = await UserService.get_user_by_id({% if cookiecutter.include_database == "y" %}db, {% endif %}user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate{% if cookiecutter.include_database == "y" %}, db: AsyncSession = Depends(get_db){% endif %}):
    """Create a new user"""
    try:
        return await UserService.create_user({% if cookiecutter.include_database == "y" %}db, {% endif %}user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate{% if cookiecutter.include_database == "y" %}, db: AsyncSession = Depends(get_db){% endif %}):
    """Update a user"""
    try:
        user = await UserService.update_user({% if cookiecutter.include_database == "y" %}db, {% endif %}user_id, user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int{% if cookiecutter.include_database == "y" %}, db: AsyncSession = Depends(get_db){% endif %}):
    """Delete a user"""
    deleted = await UserService.delete_user({% if cookiecutter.include_database == "y" %}db, {% endif %}user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return None
{%- endif %}
