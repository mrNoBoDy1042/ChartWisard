from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    metabase_url = Column(String, index=True)
    access_token = Column(String)

    questions = relationship('Question', back_populates='created_by')


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(String)
    metabase_database_id = Column(Integer)
    result_query = Column(String)
    created_by_id = Column(Integer, ForeignKey('users.id'))

    created_by = relationship('User', back_populates='questions')
