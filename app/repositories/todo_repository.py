from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo


class TodoRepository:
    """Todo data access layer"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_todo(
        self,
        title: str,
        description: Optional[str],
        user_id: int,
        due_date: Optional[datetime] = None,
    ) -> Todo:
        """Create a new todo item"""

        todo = Todo(
            title=title,
            description=description,
            user_id=user_id,
            due_date=due_date,
        )
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def get_todo_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
        """Get a todo by ID — only if it belongs to the user"""

        query = select(Todo).where((Todo.id == todo_id) & (Todo.user_id == user_id))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_todos_by_user(
        self,
        user_id: int,
        completed: Optional[bool] = None,
        due_before: Optional[datetime] = None,
        due_after: Optional[datetime] = None,
    ) -> Sequence[Todo]:
        """Get all todos for a user — latest first"""

        query = (
            select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_todo(self, todo_id: int, user_id: int, **kwargs) -> Optional[Todo]:
        """Update a todo — only if the user owns it"""

        todo = await self.get_todo_by_id(todo_id, user_id)
        if not todo:
            return None

        for key, value in kwargs.items():
            setattr(todo, key, value)

        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def delete_todo(self, todo_id: int, user_id: int) -> bool:
        """Delete a todo — only if the user owns it"""

        todo = await self.get_todo_by_id(todo_id, user_id)
        if not todo:
            return False

        await self.db.delete(todo)
        await self.db.commit()
        return True
