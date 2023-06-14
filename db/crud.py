from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, schemas


async def get_user_by_email(db: AsyncSession, email: str) -> models.User:
    result = await db.scalar(
        select(models.User).where(
            models.User.email == email
        )
    )
    return result


async def update_user_access_token(db: AsyncSession, user: models.User, access_token: str):
    await db.execute(
        select(models.User).where(models.User.email == user.email).update(
            {models.User.access_token: access_token}
        )
    )
    await db.refresh(user)
    return user



async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        metabase_url=user.metabase_url,
        email=user.email,
        access_token=user.access_token,
        hashed_password=user.metabase_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


def get_questions(
    db: AsyncSession, user: models.User, 
    skip: int = 0, limit: int = 100
):
    return db.query(models.Question)\
        .filter(models.Question.created_by_id == user.email)\
        .offset(skip).limit(limit).all()


def create_question(db: AsyncSession, question: schemas.QuestionCreate, user_id: int):
    db_item = models.Question(**question.dict(), created_by_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item