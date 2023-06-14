from typing import List

from pydantic import BaseModel
from fastapi_users.schemas import CreateUpdateDictModel


class QuestionBase(BaseModel):
    user_question: str
    metabase_database_id: str
    result_query: str = None
    created_by_id: int


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    metabase_url: str
    access_token: str


class UserCreate(CreateUpdateDictModel, BaseModel):
    email: str
    metabase_url: str
    metabase_password: str
    access_token: str = None


class User(UserBase):
    id: int
    questions: List[Question] = []

    class Config:
        orm_mode = True


class UserRead(User):
    class Config:
        fields = {
            'access_token': {'exclude': True},
        }


class SessionData(BaseModel):
    email: str