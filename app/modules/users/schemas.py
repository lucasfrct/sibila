from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from app.db.models import Role

ROLES_FIELD_DEFAULT: list[str] = []


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    is_active: bool
    roles: list[str] = ROLES_FIELD_DEFAULT

    @field_validator("roles", mode="before")
    @classmethod
    def roles_to_names(cls, value: list[Role] | list[str]) -> list[str]:
        return [item.name if isinstance(item, Role) else item for item in value]
