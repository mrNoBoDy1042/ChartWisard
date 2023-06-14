import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase, DatabaseStrategy
)
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from app.config import settings
from db.models import AccessToken, User
from db.schemas import UserCreate
from db.dependencies import get_user_db, get_access_token_db
from vendors.metabase import MetabaseAPI


SECRET = "SECRET"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    
    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        # existing_user = await self.user_db.get_by_email(user_create.email)
        # if existing_user is not None:
        #     raise exceptions.UserAlreadyExists()

        try:
            access_token = 'fake'
            # MetabaseAPI.authorize(
            #     email=user_create.email,
            #     password=user_create.metabase_password,
            #     url=user_create.metabase_url,
            # )
        except Exception:
            raise exceptions.UserNotExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop('metabase_password')
        user_dict['hashed_password'] = self.password_helper.hash(password)
        user_dict['access_token'] = access_token

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user    

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=1209600)


cookie_transport = CookieTransport(
    cookie_name=settings.app_name,
)


auth_backend = AuthenticationBackend(
    name='cookie',
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
