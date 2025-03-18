from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud.item_crud import get_todo_item, create_todo_item, update_todo_item, delete_todo_item, get_all_todo_items
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem, ResponseTodoItem
from typing import List

router = APIRouter(
    prefix="/lists/{todo_list_id}/items",
    tags=["Todo項目"],
)

@router.get("/{todo_item_id}", response_model=ResponseTodoItem)
def read_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    db_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_item is None:
        # raise HTTPException(status_code=404, detail="Todoアイテムが見つかりません")
        raise HTTPException(status_code=404)
    return db_item

@router.post("/", response_model=ResponseTodoItem)
def create_item(todo_list_id: int, new_todo_item: NewTodoItem, db: Session = Depends(get_db)):
    db_item = create_todo_item(db, todo_list_id, new_todo_item)
    if db_item is None:
        # raise HTTPException(status_code=404, detail="指定された Todo リストが見つかりません")
        raise HTTPException(status_code=404)
    return db_item

@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def update_item(todo_list_id: int, todo_item_id: int, update_todo_items: UpdateTodoItem, db: Session = Depends(get_db)):
    updated = update_todo_item(db, todo_list_id, todo_item_id, update_todo_items)
    if updated is None:
        # raise HTTPException(status_code=404, detail="Todoアイテムが見つかりません")
        raise HTTPException(status_code=404)
    return updated

@router.delete("/{todo_item_id}")
def remove_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    if not delete_todo_item(db, todo_list_id, todo_item_id):
        # raise HTTPException(status_code=404, detail="Todoアイテムが見つかりません")
        raise HTTPException(status_code=404)
    return {}

@router.get("/", response_model=List[ResponseTodoItem])
def get_todo_items(
    todo_list_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db: Session = Depends(get_db)
    ):
    """TODOリストに紐づくTODO項目の一覧を取得"""
    return get_all_todo_items(db, todo_list_id, page, per_page)