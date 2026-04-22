from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """User data access layer"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(
        self, username: str, email: str, hashed_password: str
    ) -> User:
        """Create new user"""

        user = User(username=username, email=email, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""

        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""

        return await self.db.get(User, user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by emil"""

        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()
