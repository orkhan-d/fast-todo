import os
from app.db import session
from app.todos.models import Todo

def get_todos(user_id: int):
    return session.query(Todo).filter(Todo.user_id==user_id).all()

def add_todo(user_id: int, text: str):
    todo = Todo(user_id=user_id, text=text)
    session.add(todo)
    session.commit()

    return get_todos(user_id)

def toggle_todo(id: int):
    todo = session.query(Todo).filter(Todo.id==id).one()
    todo.done = not todo.done
    session.commit()

def delete_todo(id: int):
    todo = session.query(Todo).filter(Todo.id==id).one()
    session.delete(todo)
    session.commit()