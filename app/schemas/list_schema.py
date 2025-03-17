from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, title="Todo List Description", min_length=1, max_length=200)

class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""
    title: Optional[str] = Field(default=None, title="Todo List Title", min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, title="Todo List Description", min_length=1, max_length=200)

class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""
    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, title="Todo List Description", min_length=1, max_length=200)
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")

    class Config:
        from_attributes = True