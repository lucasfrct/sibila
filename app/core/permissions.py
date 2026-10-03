import uuid
from collections.abc import Awaitable, Callable
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.models import Role, User
from app.db.session import get_db

TOKEN_URL = "/auth/login"
ERROR_CREDENTIALS_INVALID = "Could not validate credentials"
ERROR_PERMISSION_DENIED = "Permission denied"
ROLE_NAME_ADMIN = "admin"
PERMISSION_NAME_IS_ADMIN = "*"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

TokenDep = Annotated[str, Depends(oauth2_scheme)]
SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(token: TokenDep, session: SessionDep) -> User:
    try:
        payload: dict = decode_access_token(token)
        sub: str | None = payload.get("sub")
    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_CREDENTIALS_INVALID
        ) from exc

    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_CREDENTIALS_INVALID
        )

    try:
        user_id: uuid.UUID = uuid.UUID(sub)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_CREDENTIALS_INVALID
        ) from exc

    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles).selectinload(Role.permissions))
    )
    user: User | None = (await session.execute(stmt)).scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_CREDENTIALS_INVALID
        )

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def require_permission(permission_name: str) -> Callable[..., Awaitable[User]]:
    async def dependency(user: CurrentUserDep) -> User:
        if _has_permission(user, permission_name):
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_PERMISSION_DENIED
        )

    return dependency


def _has_permission(user: User, permission_name: str) -> bool:
    return any(
        _role_grants(role, permission_name) for role in user.roles
    )


def _role_grants(role: Role, permission_name: str) -> bool:
    if role.name == ROLE_NAME_ADMIN:
        return True
    return any(
        permission.name in (permission_name, PERMISSION_NAME_IS_ADMIN)
        for permission in role.permissions
    )


def user_is_admin(user: User) -> bool:
    return any(role.name == ROLE_NAME_ADMIN for role in user.roles)


def default_token_expires_delta() -> timedelta:
    return timedelta(minutes=settings.jwt_expire_minutes)
