from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


def get_todo_service(db: AsyncSession = Depends(get_db)) -> TodoService:
    """Dependency: inject TodoService with a database session"""
    repo = TodoRepository(db)
    return TodoService(repo)


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
)
async def create_todo(
    todo_create: TodoCreate,
    current_user_id: int = Depends(get_current_user),  # Authentication required!
    service: TodoService = Depends(get_todo_service),
):
    """Create a new todo item for the authenticated user."""
    return await service.create_todo(todo_create, current_user_id)


@router.get(
    "",
    response_model=list[TodoResponse],
    summary="List todos with optional filters and pagination",
)
async def list_todos(
    # --- Filtering ---
    completed: Optional[bool] = Query(
        default=None,
        description="Filter by completion status: true or false",
    ),
    due_before: Optional[datetime] = Query(
        default=None,
        description="Return todos due before this datetime (ISO 8601)",
    ),
    due_after: Optional[datetime] = Query(
        default=None,
        description="Return todos due after this datetime (ISO 8601)",
    ),
    # --- Pagination ---
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of records to skip (offset)",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of records to return (max 100)",
    ),
    # --- Auth & service ---
    current_user_id: int = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """
    Get todos for the authenticated user.

    Supports filtering by:
    - **completed**: `true` or `false`
    - **due_before**: ISO 8601 datetime, e.g. `2026-12-31T23:59:59`
    - **due_after**: ISO 8601 datetime

    Supports pagination via **skip** and **limit**.
    """
    return await service.list_todos(
        user_id=current_user_id,
        completed=completed,
        due_before=due_before,
        due_after=due_after,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Get a single todo",
)
async def get_todo(
    todo_id: int,
    current_user_id: int = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """Get a single todo by ID."""
    return await service.get_todo(todo_id, current_user_id)


@router.patch(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Partially update a todo",
)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user_id: int = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """
    Partially update a todo. Only fields included in the request body are changed.

    For example, sending `{"completed": true}` only marks it complete —
    title, description and due_date are left untouched.
    """
    return await service.update_todo(todo_id, current_user_id, todo_update)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
)
async def delete_todo(
    todo_id: int,
    current_user_id: int = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    """Delete a todo by ID"""
    await service.delete_todo(todo_id, current_user_id)
