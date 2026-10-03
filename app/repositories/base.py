from typing import Generic, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class GenericRepository(Generic[T]):
    def __init__(self, model: type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, id: str) -> T | None:
        stmt = select(self.model).where(self.model.id == id)
        result: T | None = (await self.session.execute(stmt)).scalar_one_or_none()
        return result

    async def list(self, skip: int = 0, limit: int = 100) -> list[T]:
        stmt = select(self.model).offset(skip).limit(limit)
        results: list[T] = list((await self.session.execute(stmt)).scalars().all())
        return results

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: str, data: dict) -> T | None:
        stmt = update(self.model).where(self.model.id == id).values(**data)
        await self.session.execute(stmt)
        return await self.get_by_id(id)

    async def delete(self, id: str) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return bool(result.rowcount)
