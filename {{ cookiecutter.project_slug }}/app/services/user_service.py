{% if cookiecutter.include_example == "y" -%}
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate, UserUpdate


class UserService:
    @staticmethod
    async def get_all_users(db: AsyncSession) -> List[User]:
        """Get all users"""
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get a specific user by ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get a user by email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if email already exists
        existing_user = await UserService.get_user_by_email(db, user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        new_user = User(
            name=user_data.name,
            email=user_data.email
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update a user"""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        
        # Check if email already exists (if email is being updated)
        if user_data.email:
            existing_user = await UserService.get_user_by_email(db, user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")
        
        # Update fields if provided
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        
        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """Delete a user"""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return False
        
        await db.delete(user)
        await db.commit()
        
        return True
{% else -%}
# In-memory storage for demo purposes
users_db = []
user_id_counter = 1


class UserService:
    @staticmethod
    async def get_all_users() -> List[User]:
        """Get all users"""
        return users_db

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        """Get a specific user by ID"""
        user = next((user for user in users_db if user.id == user_id), None)
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get a user by email"""
        user = next((user for user in users_db if user.email == email), None)
        return user

    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        """Create a new user"""
        global user_id_counter
        
        # Check if email already exists
        if any(u.email == user_data.email for u in users_db):
            raise ValueError("Email already registered")
        
        new_user = User(
            id=user_id_counter,
            name=user_data.name,
            email=user_data.email,
            created_at=datetime.now()
        )
        
        users_db.append(new_user)
        user_id_counter += 1
        
        return new_user

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update a user"""
        user_index = next((i for i, u in enumerate(users_db) if u.id == user_id), None)
        if user_index is None:
            return None
        
        # Check if email already exists (if email is being updated)
        if user_data.email and any(u.email == user_data.email and u.id != user_id for u in users_db):
            raise ValueError("Email already registered")
        
        user_data_obj = users_db[user_index]
        
        # Update fields if provided
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user_data_obj, field, value)
        
        user_data_obj.updated_at = datetime.now()
        
        return user_data_obj

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """Delete a user"""
        user_index = next((i for i, u in enumerate(users_db) if u.id == user_id), None)
        if user_index is None:
            return False
        
        users_db.pop(user_index)
        return True
{%- endif %}
