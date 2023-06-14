from uuid import UUID

from fastapi import APIRouter, Response, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import crud, schemas
from db.dependencies import get_async_session
from routes import cookie
from vendors.metabase import MetabaseAPI

from .dependencies import current_active_user


router = APIRouter(
    prefix='/api',
    tags=['api', 'users'],
)


# Sign Up
@router.post(
    '/users/', 
    response_model=schemas.UserRead,
    dependencies=[],
)
async def signup(
    user: schemas.UserCreate, 
    response: Response,
    db: AsyncSession = Depends(get_async_session),
):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=403)
    
    try:
        access_token = MetabaseAPI.authorize(
            email=user.email,
            password=user.metabase_password,
            url=user.metabase_url,
        )
    except Exception:
        raise HTTPException(status_code=401)
    user.access_token = access_token
    db_user = await crud.create_user(db=db, user=user)
    return db_user


# Get current user
@router.get(
    '/users/me/', 
    response_model=schemas.UserRead,
)
def current_user(
    current_user: schemas.User = Depends(current_active_user)
):
    return current_user


@router.post('/users/logout/')
async def logout_user(
    response: Response, 
    session_id: UUID = Depends(cookie),
):
    return
