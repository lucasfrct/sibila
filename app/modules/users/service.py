from app.core.security import hash_password
from app.db.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserUpdate

ERROR_USERNAME_TAKEN = "Username already registered"
ERROR_EMAIL_TAKEN = "Email already registered"


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create(self, data: UserCreate, role_names: list[str] | None = None) -> User:
        await self._ensure_unique(username=data.username, email=data.email)
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            is_active=data.is_active,
        )
        user.roles = await self.repository.get_roles_by_names(role_names or [])
        return await self.repository.create(user)

    async def get(self, id: str) -> User | None:
        return await self.repository.get_with_roles(id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.repository.list(skip=skip, limit=limit)

    async def update(self, id: str, data: UserUpdate) -> User | None:
        user = await self.repository.get_by_id(id)
        if user is None:
            return None
        fields = self._build_update_fields(data)
        await self._ensure_unique(
            username=fields.get("username"),
            email=fields.get("email"),
            exclude_id=id,
        )
        return await self.repository.update(id, fields)

    async def delete(self, id: str) -> bool:
        return await self.repository.delete(id)

    def _build_update_fields(self, data: UserUpdate) -> dict[str, str | bool]:
        fields: dict[str, str | bool] = {
            key: value
            for key, value in data.model_dump(exclude_unset=True).items()
            if value is not None
        }
        password = fields.pop("password", None)
        if password is not None:
            fields["hashed_password"] = hash_password(str(password))
        return fields

    async def _ensure_unique(
        self,
        username: str | None,
        email: str | None,
        exclude_id: str | None = None,
    ) -> None:
        if username is not None:
            existing = await self.repository.get_by_username(username)
            if existing is not None and str(existing.id) != exclude_id:
                raise ValueError(ERROR_USERNAME_TAKEN)
        if email is not None:
            existing = await self.repository.get_by_email(email)
            if existing is not None and str(existing.id) != exclude_id:
                raise ValueError(ERROR_EMAIL_TAKEN)
