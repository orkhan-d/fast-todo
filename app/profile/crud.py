import os
from fastapi import HTTPException
from sqlalchemy import and_
from app.profile.models import Profile
from app.db import session

def update_user_profile(user_id: int, data: dict):
    session.query(Profile).filter(Profile.user_id==user_id).update(data)
    session.commit()

    return True

def get_user_profile(user_id: int):
    profile = session.query(Profile).filter(Profile.user_id==user_id).first()
    if not profile:
        profile = Profile(user_id=user_id)
        session.add(profile)
        session.commit()
        session.flush([profile])
    return profile