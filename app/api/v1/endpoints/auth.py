from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Dependency: inject UserService with a database session"""
    repo = UserRepository(db)
    return UserService(repo)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_create: UserCreate, service: UserService = Depends(get_user_service)
):
    """
    Register a new user.

    - **username**: 3-50 chars, must be unique
    - **email**: valid email address, must be unique
    - **password**: minimum 8 characters, maximum 72 characters

    Returns the created user object (password is never returned).
    """
    return await service.register_user(user_create)


@router.post("/login", response_model=Token, summary="Login and get a JWT token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    """
    Authenticate with email and password, receive a JWT access token.

    - **username field**: enter your email address here (OAuth2 form convention)
    - **password**: your account password

    Returns a JWT token and basic user info.
    """

    token, user = await service.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    return {"access_token": token, "user": user}
