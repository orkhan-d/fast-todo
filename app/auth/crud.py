import os
from fastapi import HTTPException
from sqlalchemy import and_
from app.auth.models import User
from app.db import session
import jwt

def get_user_by_email(email: str):
    return session.query(User).filter(User.email==email).first()

def add_user(email: str, password: str):
    if get_user_by_email(email):
        raise Exception('E-mail уже зарегистрирован!')
    user = User(email=email, password=password)
    session.add(user)
    session.commit()

def get_user_by_id(id_: int):
    return session.query(User).filter(User.id_==id_).first()

def get_user_by_access_token(access_token: str):
    access_token = access_token.replace('Bearer', '').strip()
    user = session.query(User).filter(User.access_token==access_token).first()
    return user

def logout_user(access_token: str | None):
    if access_token:
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
            'email': user.email,
        }, os.getenv('JWT_SECRET'), algorithm="HS256") # type: ignore
        user.access_token = token
        session.commit()

        return user