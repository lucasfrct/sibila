from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import SessionLocal

SQL_SET_CURRENT_USER_ID = "SELECT set_config('app.current_user_id', :uid, true)"
SQL_SET_IS_ADMIN = "SELECT set_config('app.is_admin', :flag, true)"


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def apply_rls_context(session: AsyncSession, user_id: str, is_admin: bool) -> None:
    await session.execute(text(SQL_SET_CURRENT_USER_ID), {"uid": user_id})
    await session.execute(text(SQL_SET_IS_ADMIN), {"flag": str(is_admin).lower()})
