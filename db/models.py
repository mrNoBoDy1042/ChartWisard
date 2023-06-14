from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTableUUID,
)
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'user'

    email = Column(String, unique=True, index=True)
    metabase_url = Column(String)
    access_token = Column(String)

    questions = relationship('Question', back_populates='created_by')


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(String)
    metabase_database_id = Column(Integer)
    result_query = Column(String)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))

    created_by = relationship('User', back_populates='questions')


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass