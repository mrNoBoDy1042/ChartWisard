import json

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from app.config import settings
from db import models
from db.database import engine
from db.dependencies import create_db_and_tables
from db.schemas import UserRead, UserCreate
from routes import frontend, questions, users
from routes.dependencies import auth_backend, fastapi_users


app = FastAPI()


app.include_router(frontend.router)
app.include_router(users.router)
app.include_router(questions.router)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


app.mount(
    '/static',
    StaticFiles(directory=settings.root_path / 'frontend/static/'),
    name='static',
)


@app.on_event("startup")
async def on_startup():
    json.dump(
        get_openapi(
        title='The ChartWizard Info API',
        version='1.0',
        routes=app.routes,
        ),
        open('openapi.json', 'w'),
    )
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()