from app.core.security import verify_password
from app.db.models import User
from app.modules.users.repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self.repository.get_by_username(username)
        if user is None or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
