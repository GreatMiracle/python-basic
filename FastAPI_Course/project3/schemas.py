# todo_app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 0
    completed: bool = False

class TodoCreate(TodoBase):
    pass  # Dùng để tạo mới

class TodoUpdate(TodoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Cho phép map từ SQLAlchemy object