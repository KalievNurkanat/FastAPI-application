from core.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas import UserCreate


async def get_users(
        session: AsyncSession
) -> list[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
        session: AsyncSession,
        user_create: UserCreate
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user