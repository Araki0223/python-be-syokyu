from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud.list_crud import get_todo_list, create_todo_list, update_todo_list, delete_todo_list, get_all_todo_lists
from app.schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList
from typing import List

router = APIRouter(
    prefix="/lists",
    tags=["Todoリスト"],
)

@router.get("/", response_model=List[ResponseTodoList])
def get_todo_lists(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db: Session = Depends(get_db)):
    """TODOリストの一覧を取得"""
    return get_all_todo_lists(db, page, per_page)

@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def read_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = get_todo_list(db, todo_list_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_item

@router.post("/", response_model=ResponseTodoList)
def create_list(new_todo_list: NewTodoList, db: Session = Depends(get_db)):
    return create_todo_list(db, new_todo_list)

@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def update_list(todo_list_id: int, update_data: UpdateTodoList, db: Session = Depends(get_db)):
    updated = update_todo_list(db, todo_list_id, update_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated

@router.delete("/{todo_list_id}")
def remove_list(todo_list_id: int, db: Session = Depends(get_db)):
    if not delete_todo_list(db, todo_list_id):
        raise HTTPException(status_code=404, detail="Not Found")
    return {}