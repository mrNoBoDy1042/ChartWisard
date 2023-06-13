import json

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from db import models
from db.database import engine
from routes import frontend, questions, users
from config import settings


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(frontend.router)
app.include_router(users.router)
app.include_router(questions.router)


app.mount(
    '/static',
    StaticFiles(directory=settings.root_path / 'frontend/static/'),
    name='static',
)
app.mount(
    '/static/js',
    StaticFiles(directory=settings.root_path / 'frontend/js/'),
    name='js',
)


json.dump(
    get_openapi(
       title='The ChartWizard Info API',
       version='1.0',
       routes=app.routes,
    ),
    open('openapi.json', 'w'),
)
