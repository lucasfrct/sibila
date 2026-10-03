from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Role, User
from app.repositories.base import GenericRepository


class UserRepository(GenericRepository[User]):
    async def get_by_username(self, username: str) -> User | None:
        stmt = (
            select(User)
            .where(User.username == username)
            .options(selectinload(User.roles).selectinload(Role.permissions))
        )
        result: User | None = (await self.session.execute(stmt)).scalar_one_or_none()
        return result

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result: User | None = (await self.session.execute(stmt)).scalar_one_or_none()
        return result

    async def get_with_roles(self, id: str) -> User | None:
        stmt = (
            select(User)
            .where(User.id == id)
            .options(selectinload(User.roles).selectinload(Role.permissions))
        )
        result: User | None = (await self.session.execute(stmt)).scalar_one_or_none()
        return result

    async def get_roles_by_names(self, names: list[str]) -> list[Role]:
        if not names:
            return []
        stmt = select(Role).where(Role.name.in_(names))
        results: list[Role] = list((await self.session.execute(stmt)).scalars().all())
        return results
