import os
from fastapi import HTTPException
from sqlalchemy import and_
from app.auth.models import User
from app.db import session
import jwt

def get_user_by_email(email: str):
    return session.query(User).filter(User.email==email).first()

def add_user(name: str, email: str, password: str):
    user = User(name=name, email=email, password=password)
    session.add(user)
    session.commit()

def get_user_by_id(id_: int):
    return session.query(User).filter(User.id_==id_).first()

def logout_user(access_token: str):
    user = session.query(User).filter(User.access_token==access_token).first()
    if user:
        user.access_token = None
        session.commit()

def login_user(email: str, password: str):
    user = session.query(User).filter(and_(
        User.email==email,
        User.password==password,
    )).first()

    if user:
        token = jwt.encode({
            'id': user.id_,
            'name': user.name,
            'email': user.email,
        }, os.getenv('JWT_SECRET'), algorithm="HS256") # type: ignore
        user.access_token = token
        session.commit()

        return user
    else:
        raise HTTPException(401, {
            'message': 'Authorization error'
        })