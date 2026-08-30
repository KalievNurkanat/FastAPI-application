from typing import Annotated

from core.models.db_helper import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.schemas import UserCreate, UserRead

router = APIRouter(tags=["Users"])


@router.get("/get_users", response_model=list[UserRead])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> list[UserRead]:
    return await crud.get_users(session=session)


@router.post("/create_user", response_model=UserCreate)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: UserCreate
) -> UserCreate:
    return await crud.create_user(
        session=session,
        user_create=user
    )