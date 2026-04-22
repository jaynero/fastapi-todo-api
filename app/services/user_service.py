from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """User business logic"""

    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, user_create: UserCreate):
        """Register new user with validation"""
        # Check username not taken
        existing = await self.repo.get_user_by_username(user_create.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

        # Check email not taken
        existing_email = await self.repo.get_user_by_email(user_create.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Hash password and save
        hashed = hash_password(user_create.password)
        return await self.repo.create_user(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed,
        )

    async def authenticate_user(self, email: str, password: str):
        """Authenticate user and return JWT token"""
        # Find user
        user = await self.repo.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Create token
        token = create_access_token(data={"sub": str(user.id)})
        return token, user

    async def get_user(self, user_id: int):
        """Fetch user by ID"""
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
