from sqlalchemy.orm import Session
from app.models.list_model import ListModel
from app.schemas.list_schema import NewTodoList, UpdateTodoList

def get_todo_list(db: Session, todo_list_id: int):
    """指定されたIDのTODOリストを取得"""
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()

def create_todo_list(db: Session, new_todo_list: NewTodoList):
    """新しいTODOリストを作成"""
    db_item = ListModel(**new_todo_list.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_todo_list(db: Session, todo_list_id: int, update_todo_list: UpdateTodoList):
    """指定されたIDのTODOリストを更新"""
    db_item = get_todo_list(db, todo_list_id)
    if db_item is None:
        return None
    
    update_data = update_todo_list.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

def delete_todo_list(db: Session, todo_list_id: int):
    """指定されたIDのTODOリストを削除"""
    db_item = get_todo_list(db, todo_list_id)
    if db_item is None:
        return None
    
    db.delete(db_item)
    db.commit()
    return True

def get_all_todo_lists(db: Session, page: int, per_page: int):
    """TODOリストを全件取得"""
    offset = (page - 1) * per_page
    return db.query(ListModel).offset(offset).limit(per_page).all()