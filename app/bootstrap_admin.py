"""Bootstrap do usuário administrador inicial (idempotente).

Executado automaticamente junto com as migrations (migrations/env.py).
Execução manual: uv run python -m app.bootstrap_admin
"""

import asyncio

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.permissions import ROLE_NAME_ADMIN
from app.core.security import hash_password
from app.db.models import Permission, Role, User
from app.db.seeds import FIRST_ADMIN_EMAIL, FIRST_ADMIN_PASSWORD, FIRST_ADMIN_USERNAME
from app.db.session import SQL_SET_IS_ADMIN
from app.modules.users.controller import (
    PERMISSION_USERS_CREATE,
    PERMISSION_USERS_DELETE,
    PERMISSION_USERS_READ,
    PERMISSION_USERS_UPDATE,
)

ROLE_NAME_USER = "user"

DEFAULT_PERMISSIONS: tuple[tuple[str, str], ...] = (
    (PERMISSION_USERS_CREATE, "Allows creating users"),
    (PERMISSION_USERS_READ, "Allows reading users"),
    (PERMISSION_USERS_UPDATE, "Allows updating users"),
    (PERMISSION_USERS_DELETE, "Allows deleting users"),
)

MSG_ADMIN_ALREADY_EXISTS = "Admin user '{username}' already exists; nothing to do."
MSG_BOOTSTRAP_OK = "Bootstrap complete: admin user '{username}' created with role 'admin'."
MSG_CREATED_ROLE = "Created role '{name}'."
MSG_CREATED_PERMISSION = "Created permission '{name}'."


async def _get_or_create_role(session: AsyncSession, name: str) -> Role:
    stmt = select(Role).where(Role.name == name).options(selectinload(Role.permissions))
    role: Role | None = (await session.execute(stmt)).scalar_one_or_none()
    if role is not None:
        return role
    role = Role(name=name, permissions=[])
    session.add(role)
    print(MSG_CREATED_ROLE.format(name=name))
    return role


async def _get_or_create_permission(
    session: AsyncSession, name: str, description: str
) -> Permission:
    stmt = select(Permission).where(Permission.name == name)
    permission: Permission | None = (await session.execute(stmt)).scalar_one_or_none()
    if permission is not None:
        return permission
    permission = Permission(name=name, description=description)
    session.add(permission)
    print(MSG_CREATED_PERMISSION.format(name=name))
    return permission


async def _get_or_create_default_permissions(session: AsyncSession) -> list[Permission]:
    return [
        await _get_or_create_permission(session, name, description)
        for name, description in DEFAULT_PERMISSIONS
    ]


def _link_permissions(role: Role, permissions: list[Permission]) -> None:
    linked_names = {permission.name for permission in role.permissions}
    for permission in permissions:
        if permission.name not in linked_names:
            role.permissions.append(permission)


async def _find_admin_user(session: AsyncSession) -> User | None:
    stmt = (
        select(User)
        .where(User.username == FIRST_ADMIN_USERNAME)
        .options(selectinload(User.roles))
    )
    user: User | None = (await session.execute(stmt)).scalar_one_or_none()
    return user


def _build_admin_user(admin_role: Role) -> User:
    return User(
        username=FIRST_ADMIN_USERNAME,
        email=FIRST_ADMIN_EMAIL,
        hashed_password=hash_password(FIRST_ADMIN_PASSWORD),
        is_active=True,
        roles=[admin_role],
    )


async def main() -> None:
    async with SessionLocal() as session, session.begin():
        await session.execute(text(SQL_SET_IS_ADMIN), {"flag": "true"})

        admin_role = await _get_or_create_role(session, ROLE_NAME_ADMIN)
        await _get_or_create_role(session, ROLE_NAME_USER)
        permissions = await _get_or_create_default_permissions(session)
        _link_permissions(admin_role, permissions)

        existing_user = await _find_admin_user(session)
        if existing_user is not None:
            print(MSG_ADMIN_ALREADY_EXISTS.format(username=FIRST_ADMIN_USERNAME))
            return

        session.add(_build_admin_user(admin_role))

    print(MSG_BOOTSTRAP_OK.format(username=FIRST_ADMIN_USERNAME))


if __name__ == "__main__":
    asyncio.run(main())
