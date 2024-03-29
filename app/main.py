import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from app.auth.routes import router as authRouter
# from app.profile.routes import router as profileRouter
from app.todos.routes import router as todosRouter, main_router
from app.categories.routes import router as categoriesRouter

app = FastAPI(debug=True)
app.mount('/static', StaticFiles(directory=os.path.join('app', 'static')))

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)

app.include_router(authRouter)
# app.include_router(profileRouter)
app.include_router(todosRouter)
app.include_router(categoriesRouter)
app.include_router(main_router)