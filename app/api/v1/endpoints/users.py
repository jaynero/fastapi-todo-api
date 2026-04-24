from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Dependency: inject UserService with a database session"""
    repo = UserRepository(db)
    return UserService(repo)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_current_user_profile(
    current_user_id: int = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """
    Returns the profile of the currently authenticated user.

    Requires a valid JWT token in the Authorization header.
    """
    return await service.get_user(current_user_id)
