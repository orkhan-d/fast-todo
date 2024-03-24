import os
from fastapi import APIRouter, Form, Header, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Annotated

from app.auth.crud import add_user, login_user, logout_user
from app.auth.schemas import LoginSchema, RegisterSchema

templates = Jinja2Templates(os.path.join('app', 'auth', 'templates'))
router = APIRouter(prefix='/auth')

@router.get('/login')
async def login_page(request: Request):
    return templates.TemplateResponse(
        request, 'login.html'
    )

@router.post('/login')
async def login(request: Request, form: LoginSchema = Depends(LoginSchema.as_form)):
    res = login_user(**form.model_dump())
    if res:
        response = templates.TemplateResponse(
            request, 'login.html'
        )
        response.set_cookie('access-token', res.access_token)
    else:
        response = templates.TemplateResponse(
            request, 'login.html', {
                'errors': ['Неверные данные']
            }
        )

    return response

@router.get('/logout')
async def logout(request: Request):
    token = request.cookies.get('access-token')
    logout_user(token)
    response = RedirectResponse('/auth/login')
    response.delete_cookie("access-token")
    return response

@router.get('/register')
async def register_page(request: Request):
    return templates.TemplateResponse(
        request, 'register.html'
    )

@router.post('/register')
async def register(request: Request, form: RegisterSchema = Depends(RegisterSchema.as_form)):
    add_user(**form.model_dump())
    res = login_user(form.email, form.password)

    response = JSONResponse(res.as_dict(), 201)
    response.set_cookie('access-token', res.access_token)
    return response