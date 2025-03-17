from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.const import TodoItemStatusCode

class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: Optional[datetime] = Field(default=None, title="Todo Item Due")

class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""
    title: Optional[str] = Field(default=None, title="Todo Item Title", min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: Optional[datetime] = Field(default=None, title="Todo Item Due")
    complete: Optional[bool] = Field(default=None, title="Set Todo Item status as completed")

class ResponseTodoItem(BaseModel):
    """TODO項目のレスポンススキーマ."""
    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: Optional[datetime] = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")

    class Config:
        from_attributes = True