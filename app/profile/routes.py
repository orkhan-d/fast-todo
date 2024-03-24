from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from typing import Annotated


from app.profile.crud import update_user_profile, get_user_profile
from app.auth.crud import get_user_by_access_token
from app.profile.schemas import UpdateProfileSchema

router = APIRouter(prefix='/api/profile')

@router.patch('/')
async def update_profile(data: UpdateProfileSchema, Authorization: Annotated[str | None, Header()] = None):
    update_user_profile(get_user_by_access_token(Authorization).id_, data.model_dump())
    return JSONResponse({
        'message': 'success'
    }, 200)

@router.get('/')
async def get_profile(Authorization: Annotated[str | None, Header()] = None):
    profile = get_user_profile(get_user_by_access_token(Authorization).id_)
    return JSONResponse(
        profile.as_dict()
    )