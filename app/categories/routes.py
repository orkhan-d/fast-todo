import os
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.auth.crud import get_user_by_access_token
from app.categories.schemas import AddCategorySchema
from app.categories.crud import add_category, delete_category, get_categories, get_category_tasks

templates = Jinja2Templates(os.path.join('app', 'categories', 'templates'))
router = APIRouter(prefix='/categories')

main_router = APIRouter()

@router.post('/add')
async def add_todo_route(request: Request):
    token = request.cookies.get('access-token', None)
    if not token:
        return RedirectResponse('/auth/login')
    form_data = await request.form()
    form: AddCategorySchema = AddCategorySchema(**dict(form_data.items()))

    user = get_user_by_access_token(token)
    if not user:
        response = RedirectResponse('/auth/login', 302)
        response.delete_cookie('access-token')
        return response
    add_category(user.id_, form.name)

    return RedirectResponse('/', 302)

@router.get('/')
async def todos_page(request: Request):
    token = request.cookies.get('access-token', None)
    if token:
        user = get_user_by_access_token(token)
        if not user:
            response = RedirectResponse('/auth/login', 302)
            response.delete_cookie('access-token')
            return response
        categories = get_categories(user.id_)
        return templates.TemplateResponse('main.html', context={
            'request': request,
            'categories': categories
        })
    return RedirectResponse('/auth/login')

@router.get('/{cat_id}/delete')
async def cat_delete(request: Request, cat_id: int):
    token = request.cookies.get('access-token', None)
    if token:
        delete_category(cat_id)
        user = get_user_by_access_token(token)
        if not user:
            response = RedirectResponse('/auth/login', 302)
            response.delete_cookie('access-token')
            return response
        categories = get_categories(user.id_)
        return templates.TemplateResponse('main.html', context={
            'request': request,
            'categories': categories
        })
    return RedirectResponse('/auth/login')

@router.get('/{cat_id}/todos')
async def cat_todos(request: Request, cat_id: int):
    token = request.cookies.get('access-token', None)
    if token:
        user = get_user_by_access_token(token)
        if not user:
            response = RedirectResponse('/auth/login', 302)
            response.delete_cookie('access-token')
            return response
        todos = get_category_tasks(user.id_, cat_id)
        # categories = get_categories(user.id_)
        return templates.TemplateResponse('todos.html', context={
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