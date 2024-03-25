import os
from fastapi import APIRouter, Depends, Header, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Annotated

from pydantic import ValidationError


from app.profile.crud import update_user_profile, get_user_profile
from app.auth.crud import get_user_by_access_token
from app.profile.schemas import UpdateProfileSchema

templates = Jinja2Templates(os.path.join('app', 'profile', 'templates'))
router = APIRouter(prefix='/profile')

@router.post('/')
async def update_profile(request: Request):
    token = request.cookies.get('access-token', None)
    if not token:
        return RedirectResponse('/auth/login')
    form = await request.form()
    try:
        form = UpdateProfileSchema(**dict(form.items()))
    except ValidationError as e:
        user = get_user_by_access_token(token)
        if not user:
            response = RedirectResponse('/auth/login', 302)
            response.delete_cookie('access-token')
            return response
        profile = get_user_profile(user.id_)
        return templates.TemplateResponse('profile.html', context={
            'request': request,
            'profile': profile,
            'errors': [err.get('msg') for err in e.errors()]
        })
    
    user = get_user_by_access_token(token)
    user = get_user_by_access_token(token)
    if not user:
        response = RedirectResponse('/auth/login', 302)
        response.delete_cookie('access-token')
        return response
    profile = update_user_profile(user.id_, form.model_dump())
    return templates.TemplateResponse('profile.html', context={
        'request': request,
        'profile': profile,
    })

@router.get('/')
async def get_profile(request: Request):
    token = request.cookies.get('access-token', None)
    if token:
        user = get_user_by_access_token(token)
        if not user:
            response = RedirectResponse('/auth/login', 302)
            response.delete_cookie('access-token')
            return response
        profile = get_user_profile(user.id_)
        return templates.TemplateResponse('profile.html', context={
            'request': request,
            'profile': profile,
        })
    return RedirectResponse('/auth/login')