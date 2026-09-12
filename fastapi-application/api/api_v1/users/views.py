from typing import Annotated

from core.config import settings
from core.models import db_helper
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.users import crud
from api.api_v1.users.redis_key import users_list_key_builder
from api.api_v1.users.schemas import CreateUser, ReadUser

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[ReadUser])
@cache(
    expire=50,
    key_builder=users_list_key_builder,
    namespace=settings.cache.namespace
)
async def get_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[ReadUser]:
    return await crud.get_users(session=session)


@router.post("/create", response_model=CreateUser)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_params: CreateUser
) -> CreateUser:
    return await crud.create_user(
        session=session,
        user_params=user_params
    )



