from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import CurrentUserDep, SessionDep, default_token_expires_delta
from app.core.security import create_access_token
from app.db.models import User
from app.modules.auth.schemas import TokenResponse
from app.modules.auth.service import AuthService
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserRead

TOKEN_SUB_CLAIM = "sub"
TOKEN_USERNAME_CLAIM = "username"
ERROR_INVALID_CREDENTIALS = "Incorrect username or password"

router = APIRouter(prefix="/auth", tags=["auth"])


def build_auth_service(session: AsyncSession) -> AuthService:
    return AuthService(UserRepository(User, session))


@router.post("/login", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> TokenResponse:
    service = build_auth_service(session)
    user = await service.authenticate(form.username, form.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(
        {TOKEN_SUB_CLAIM: str(user.id), TOKEN_USERNAME_CLAIM: user.username},
        default_token_expires_delta(),
    )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: CurrentUserDep) -> UserRead:
    return UserRead.model_validate(current_user)
