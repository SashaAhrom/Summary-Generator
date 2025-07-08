from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Yields a SQLAlchemyUserDatabase instance for user operations using the provided asynchronous database session.

    Args:
        session (AsyncSession, optional): The asynchronous database session dependency. Defaults to Depends(get_async_session).

    Yields:
        SQLAlchemyUserDatabase: An instance configured with the current session and User model.
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """
    Creates and returns a JWTStrategy instance configured with the application's secret and a token lifetime of 3600 seconds.

    Returns:
        JWTStrategy: An instance of JWTStrategy initialized with the specified secret and token lifetime.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",  
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    UserManager class for managing user-related operations.

    Inherits from:
        IntegerIDMixin
        BaseUserManager[User, int]

    Methods:
        async validate_password(password: str, user: Union[UserCreate, User]) -> None:
            Validates the given password for a user.
            Raises InvalidPasswordException if the password is less than 3 characters
            or contains the user's email address.

        async on_after_register(user: User, request: Optional[Request] = None):
            Called after a user has been successfully registered.
            Can be used to perform actions such as sending a welcome email.
    """
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason="Password should be at least 3 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # Вместо print здесь можно было бы настроить отправку письма.
        print(f"Пользователь {user.email} зарегистрирован.")


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Dependency function that provides a UserManager instance.

    Args:
        user_db: The user database dependency, injected via FastAPI's Depends.

    Yields:
        UserManager: An instance of UserManager initialized with the provided user_db.
    """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
