import os
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.auth.crud import get_user_by_access_token
from app.todos.schemas import AddTodoSchema
from app.todos.crud import add_todo, delete_todo, get_todos, toggle_todo

templates = Jinja2Templates(os.path.join('app', 'todos', 'templates'))
router = APIRouter(prefix='/todos')

main_router = APIRouter()

@router.post('/add')
async def add_todo_route(request: Request):
    token = request.cookies.get('access-token', None)
    if not token:
        return RedirectResponse('/auth/login')
    form_data = await request.form()
    form: AddTodoSchema = AddTodoSchema(**dict(form_data.items()))

    user = get_user_by_access_token(token)
    if not user:
        response = RedirectResponse('/auth/login', 302)
        response.delete_cookie('access-token')
        return response
    add_todo(user.id_, form.text)

    return RedirectResponse('/', 302)

@router.get('/')
@main_router.get('/')
async def todos_page(request: Request):
    token = request.cookies.get('access-token', None)
    if token:
        user = get_user_by_access_token(token)
        if not user:
            response = RedirectResponse('/auth/login', 302)
            response.delete_cookie('access-token')
            return response
        todos = get_todos(user.id_)
        return templates.TemplateResponse('main.html', context={
            'request': request,
            'todos': todos
        })
    return RedirectResponse('/auth/login')

@router.get('/{todo_id}/delete')
async def todos_delete(request: Request, todo_id: int):
    token = request.cookies.get('access-token', None)
    if token:
        delete_todo(todo_id)
        user = get_user_by_access_token(token)
        if not user:
            response = RedirectResponse('/auth/login', 302)
            response.delete_cookie('access-token')
            return response
        todos = get_todos(user.id_)
        return templates.TemplateResponse('main.html', context={
            'request': request,
            'todos': todos
        })
    return RedirectResponse('/auth/login')

@router.get('/{todo_id}/toggle')
async def todos_toggle(request: Request, todo_id: int):
    token = request.cookies.get('access-token', None)
    if token:
        toggle_todo(todo_id)
        user = get_user_by_access_token(token)
        if not user:
            response = RedirectResponse('/auth/login', 302)
            response.delete_cookie('access-token')
            return response
        todos = get_todos(user.id_)
        return templates.TemplateResponse('main.html', context={
            'request': request,
            'todos': todos
        })
    return RedirectResponse('/auth/login')

@router.get('/add')
async def todos_add_page(request: Request):
    token = request.cookies.get('access-token', None)
    if token:
        return templates.TemplateResponse('add.html', context={
            'request': request
        })
    return RedirectResponse('/auth/login')