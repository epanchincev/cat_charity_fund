from typing import Union

from fastapi import Depends
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import (JWT_LIFETIME_SECONDS, MIN_PASSWORD_LEN,
                                PASSWORD_LESS_THAN_NEED_ERROR,
                                PASSWORD_MUST_NOT_CONTAIN_EMAIL_ERROR)
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> SQLAlchemyUserDatabase:
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Стратегия хранения токена"""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=JWT_LIFETIME_SECONDS)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Валидация пароля"""
        if len(password) < MIN_PASSWORD_LEN:
            raise InvalidPasswordException(
                reason=PASSWORD_LESS_THAN_NEED_ERROR
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=PASSWORD_MUST_NOT_CONTAIN_EMAIL_ERROR
            )


async def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    """Корутина, возвращающая объект класса UserManager"""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
