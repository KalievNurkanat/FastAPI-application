from typing import Annotated

from auth.utils import hash_password
from core.models import User, db_helper
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.users.schemas import CreateUser


async def create_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_params: CreateUser,
) -> User:
    password = hash_password(
        password=user_params.password
    )
    user = User(username=user_params.username,
                password=password, 
                email=user_params.email, 
                is_active=user_params.is_active
            )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user