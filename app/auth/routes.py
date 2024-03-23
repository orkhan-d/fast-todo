from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from typing import Annotated

from app.auth.crud import add_user, login_user, logout_user
from app.auth.schemas import LoginSchema, RecoverPasswordSchema, RegisterSchema

router = APIRouter(prefix='/api/auth')

@router.post('/login')
async def login(data: LoginSchema):
    res = login_user(**data.model_dump())
    return JSONResponse(res.as_dict(), 200)

@router.get('/logout')
async def logout(Authorization: Annotated[str | None, Header()] = None):
    if not Authorization: return
    logout_user(Authorization.split()[1])
    return JSONResponse({'message': 'success'}, 201)

@router.post('/register')
async def register(data: RegisterSchema):
    add_user(**data.model_dump())
    res = login_user(data.email, data.password)
    return JSONResponse(res.as_dict(), 201)

@router.post('/recover')
async def recover(data: RecoverPasswordSchema):
    return data