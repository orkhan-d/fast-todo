import os
from app.db import session
from app.categories.models import Category
from app.todos.models import Todo

def get_categories(user_id: int):
    return session.query(Category).filter(Category.user_id==user_id).all()

def add_category(user_id: int, name: str):
    todo = Category(user_id=user_id, name=name)
    session.add(todo)
    session.commit()

    return get_categories(user_id)

def get_category_tasks(user_id: int, cat_id: int):
    return session.query(Todo).filter(Todo.user_id==user_id).filter(Todo.category_id==cat_id).all()

def delete_category(id: int):
    todo = session.query(Category).filter(Category.id_==id).one()
    session.delete(todo)
    session.commit()