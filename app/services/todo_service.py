from datetime import datetime

from fastapi import HTTPException, status

from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    """Todo business logic"""

    def __init__(self, repo: TodoRepository):
        self.repo = repo

    async def create_todo(self, todo_create: TodoCreate, user_id: int):
        """Create a new todo with validation"""
        # Validate title not empty
        if not todo_create.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty or whitespace",
            )

        return await self.repo.create_todo(
            title=todo_create.title.strip(),
            description=(
                todo_create.description.strip() if todo_create.description else None
            ),
            due_date=todo_create.due_date,
            user_id=user_id,
        )

    async def get_todo(self, todo_id: int, user_id: int):
        """Get a single todo by ID"""
        todo = await self.repo.get_todo_by_id(todo_id, user_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return todo

    async def list_todos(
        self,
        user_id: int,
        completed: bool | None = None,
        due_before: datetime | None = None,
        due_after: datetime | None = None,
    ):
        """Get all todos for the current user"""

        return await self.repo.get_todos_by_user(
            user_id=user_id,
            completed=completed,
            due_before=due_before,
            due_after=due_after,
        )

    async def update_todo(self, todo_id: int, user_id: int, todo_update: TodoUpdate):
        """Update a todo — only provided fields are changed"""
        todo = await self.repo.update_todo(
            todo_id,
            user_id,
            **todo_update.model_dump(exclude_unset=True),
        )

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return todo

    async def delete_todo(self, todo_id: int, user_id: int):
        """Delete a todo by ID"""
        deleted = await self.repo.delete_todo(todo_id, user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
