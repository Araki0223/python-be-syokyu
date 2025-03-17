from sqlalchemy.orm import Session
from app.models.item_model import ItemModel
from app.models.list_model import ListModel
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem
from app.const import TodoItemStatusCode

def get_todo_item(db: Session, todo_list_id: int, todo_item_id: int):
    """指定されたIDのTODOアイテムを取得"""
    return db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id
    ).first()

def create_todo_item(db: Session, todo_list_id: int, new_todo_item: NewTodoItem):
    """新しいTODOアイテムを作成"""
    parent_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if parent_list is None:
        return None

    db_item = ItemModel(
        todo_list_id=todo_list_id,
        title=new_todo_item.title,
        description=new_todo_item.description,
        due_at=new_todo_item.due_at,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_todo_item(db: Session, todo_list_id: int, todo_item_id: int, update_todo_item: UpdateTodoItem):
    """指定されたIDのTODOアイテムを更新"""
    db_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_item is None:
        return None

    update_data = update_todo_item.model_dump(exclude_unset=True)

    if "complete" in update_data:
        db_item.status_code = (
            TodoItemStatusCode.COMPLETED.value if update_data["complete"] else TodoItemStatusCode.NOT_COMPLETED.value
        )
        del update_data["complete"]

    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

def delete_todo_item(db: Session, todo_list_id: int, todo_item_id: int):
    """指定されたIDのTODOアイテムを削除"""
    db_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_item is None:
        return None

    db.delete(db_item)
    db.commit()
    return True

def get_all_todo_items(db: Session, todo_list_id: int):
    """指定されたTODOリストのアイテムを全件取得"""
    return db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id).all()