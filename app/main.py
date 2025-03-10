import os
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.const import TodoItemStatusCode

from .models.item_model import ItemModel
from .models.list_model import ListModel

from fastapi import Depends
from sqlalchemy.orm import Session
from .dependencies import get_db
from fastapi import HTTPException
# from datetime import datetime

DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )


class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""

    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")


class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    complete: bool | None = Field(default=None, title="Set Todo Item status as completed")


class ResponseTodoItem(BaseModel):
    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""

    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""

    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


@app.get("/echo", tags=["Hello"])
def get_hello(message: str = "Hello", name: str = "TechTrain"):
    # message = "Hello"
    # name = "TechTrain"
    return {"Message": f"{message} {name}!"}
    # return {"Message": "Hello TechTrain!"}

@app.get("/health", tags=["System"])
def get_health():
    return {"status": "ok"}

@app.get("/lists/{todo_list_id}", tags=["Todoリスト"])
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_item is None:
        return {"message": "Not Found"}
    return db_item

@app.post("/lists", tags=["Todoリスト"], response_model=ResponseTodoList)
def post_todo_list(new_todo_list: NewTodoList, db: Session = Depends(get_db)):
    db_item = ListModel(**new_todo_list.model_dump()) 
    # ListModelはNewTodoList(Pydanticモデル)で、辞書形式(dict)に変換する必要がある
    # model_dump() は NewTodoList のデータを { "title": "xxx", "description": "yyy" } の辞書に変換する。
    # ListModel(**辞書) により、辞書のキーを ListModel の引数に展開し、新しいデータベースレコードを作成 する。
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/lists/{todo_list_id}", tags=["Todoリスト"], response_model=ResponseTodoList)
def put_todo_list(update_todo_list: UpdateTodoList, todo_list_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first() # データベースからレコードを取得
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todoリストが見つかりません")  # 404エラーハンドリング

    update_data = update_todo_list.model_dump(exclude_unset=True)  # リクエストボディのデータを辞書に変換
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item