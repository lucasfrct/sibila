from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    hashed: bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(payload: dict[str, Any], expires_delta: timedelta) -> str:
    to_encode = {**payload, "exp": datetime.now(timezone.utc) + expires_delta}
    token: str = jwt.encode(to_encode, settings.jwt_secret_key, settings.jwt_algorithm)
    return token


def decode_access_token(token: str) -> dict[str, Any]:
    decoded: dict[str, Any] = jwt.decode(
        token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
    )
    return decoded
