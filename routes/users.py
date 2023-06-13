from uuid import UUID, uuid4

from fastapi import APIRouter, Response, Depends, HTTPException
from sqlalchemy.orm import Session

from db.schemas import SessionData
from db import crud, schemas
from routes import cookie
from routes.dependencies import get_db, session_backend, get_current_user
from vendors.metabase import MetabaseAPI


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
async def create_user(
    user: schemas.UserCreate, 
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        access_token = MetabaseAPI.authorize(
            email=user.email,
            password=user.metabase_password,
            url=user.metabase_url,
        )
    except Exception:
        raise HTTPException(status_code=401)

    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        user.access_token = access_token
        db_user = crud.create_user(db=db, user=user)
    else:
        db_user.access_token = access_token
        db_user.save()

    session = uuid4()
    data = SessionData(email=db_user.email)
    await session_backend.create(session, data)
    cookie.attach_to_response(response, session)
    
    return db_user


# Get current user
@router.get(
    '/users/me/', 
    response_model=schemas.UserRead,
)
def current_user(
    current_user: schemas.User = Depends(get_current_user)
):
    return current_user


@router.post('/users/logout/')
async def logout_user(
    response: Response, 
    session_id: UUID = Depends(cookie),
):
    await session_backend.delete(session_id)
    cookie.delete_from_response(response)
    return
