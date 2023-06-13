from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        metabase_url=user.metabase_url,
        email=user.email,
        access_token=user.access_token,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_questions(
    db: Session, user: models.User, 
    skip: int = 0, limit: int = 100
):
    return db.query(models.Question)\
        .filter(models.Question.created_by_id == user.email)\
        .offset(skip).limit(limit).all()


def create_question(db: Session, question: schemas.QuestionCreate, user_id: int):
    db_item = models.Question(**question.dict(), created_by_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item