from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

UsernameStr = Annotated[str, Field(min_length=3, max_length=50)]
UserEmail = Annotated[EmailStr, Field(max_length=120)]
PasswordStr = Annotated[str, Field(min_length=8, max_length=72)]


class UserBase(BaseModel):
    """Shared user properties — base for create and response schemas"""

    username: UsernameStr
    email: UserEmail


class UserCreate(UserBase):
    """Request model: new user registration"""

    password: PasswordStr


class UserResponse(UserBase):
    """Response model: user data returned to client"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class Token(BaseModel):
    """Response model: JWT token returned after successful login"""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
