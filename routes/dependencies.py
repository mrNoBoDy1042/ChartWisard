from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from sqlalchemy.orm import Session

from db import crud
from db.database import SessionLocal
from db.schemas import SessionData


session_backend = InMemoryBackend[UUID, SessionData]()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=session_backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

def get_current_user(
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(verifier),
):
    user = crud.get_user_by_email(db, email=session_data.email)
    return user