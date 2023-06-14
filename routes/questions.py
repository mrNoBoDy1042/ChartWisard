from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import crud, schemas
from db.dependencies import get_async_session
from vendors import MetabaseAPI, GPTAPI

from .dependencies import current_active_user


router = APIRouter(
    prefix='/api',
    tags=['api', 'questions'],
)

@router.get(
    '/questions/', 
    response_model=List[schemas.Question]
)
async def read_items(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_async_session),
    current_user: schemas.User = Depends(current_active_user),
):
    questions = crud.get_questions(db, user=current_user, skip=skip, limit=limit)
    return questions


@router.post(
    '/questions/', 
    response_model=schemas.Question,
)
async def ask_question(
    question: schemas.QuestionCreate, 
    db: AsyncSession = Depends(get_async_session),
    current_user: schemas.User = Depends(current_active_user),
):
    crud.create_question(db=db, question=question, user_id=current_user.id)
    metabase_adapter = MetabaseAPI()
    gpt_adapter = GPTAPI()

    database_schema = metabase_adapter.get_database_schema(
        question.metabase_database_id
    )
    sql_query = gpt_adapter.get_sql_query(
        question.user_question, 
        database_schema
    )
    query_url = metabase_adapter.get_query_url(
        question.metabase_database_id, 
        sql_query
    )

    return query_url
