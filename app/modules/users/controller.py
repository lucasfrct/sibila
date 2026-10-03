from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import SessionDep, require_permission, user_is_admin
from app.db.models import User
from app.db.session import apply_rls_context
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserRead, UserUpdate
from app.modules.users.service import UserService

PERMISSION_USERS_CREATE = "users:create"
PERMISSION_USERS_READ = "users:read"
PERMISSION_USERS_UPDATE = "users:update"
PERMISSION_USERS_DELETE = "users:delete"
ERROR_USER_NOT_FOUND = "User not found"

CreateGuard = Annotated[User, Depends(require_permission(PERMISSION_USERS_CREATE))]
ReadGuard = Annotated[User, Depends(require_permission(PERMISSION_USERS_READ))]
UpdateGuard = Annotated[User, Depends(require_permission(PERMISSION_USERS_UPDATE))]
DeleteGuard = Annotated[User, Depends(require_permission(PERMISSION_USERS_DELETE))]

router = APIRouter(prefix="/users", tags=["users"])


def build_user_service(session: AsyncSession) -> UserService:
    return UserService(UserRepository(User, session))


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    session: SessionDep,
    current_user: CreateGuard,
) -> UserRead:
    await apply_rls_context(session, str(current_user.id), user_is_admin(current_user))
    service = build_user_service(session)
    try:
        user = await service.create(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return UserRead.model_validate(user)


@router.get("/", response_model=list[UserRead])
async def list_users(
    session: SessionDep,
    current_user: ReadGuard,
    skip: int = 0,
    limit: int = 100,
) -> list[UserRead]:
    await apply_rls_context(session, str(current_user.id), user_is_admin(current_user))
    service = build_user_service(session)
    users = await service.list(skip=skip, limit=limit)
    return [UserRead.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    session: SessionDep,
    current_user: ReadGuard,
) -> UserRead:
    await apply_rls_context(session, str(current_user.id), user_is_admin(current_user))
    service = build_user_service(session)
    user = await service.get(str(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_USER_NOT_FOUND)
    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    session: SessionDep,
    current_user: UpdateGuard,
) -> UserRead:
    await apply_rls_context(session, str(current_user.id), user_is_admin(current_user))
    service = build_user_service(session)
    try:
        user = await service.update(str(user_id), data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_USER_NOT_FOUND)
    return UserRead.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    session: SessionDep,
    current_user: DeleteGuard,
) -> None:
    await apply_rls_context(session, str(current_user.id), user_is_admin(current_user))
    service = build_user_service(session)
    deleted = await service.delete(str(user_id))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_USER_NOT_FOUND)
