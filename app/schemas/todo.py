from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

# Reusable constrained types
TitleStr = Annotated[str, Field(min_length=1, max_length=150)]
DescriptionStr = Annotated[str | None, Field(default=None, max_length=500)]


class TodoBase(BaseModel):
    """Shared todo fields"""

    title: TitleStr
    description: DescriptionStr = None
    completed: bool = False
    due_date: datetime | None = None


class TodoCreate(TodoBase):
    """Request model: create a new todo"""

    pass


class TodoUpdate(BaseModel):
    """Request model: update a todo — all fields optional"""

    # Using the same constraints but ensuring they remain optional
    title: TitleStr | None = None
    description: DescriptionStr = None
    completed: bool | None = None
    due_date: datetime | None = None


class TodoResponse(TodoBase):
    """Response model: todo data returned to client"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
