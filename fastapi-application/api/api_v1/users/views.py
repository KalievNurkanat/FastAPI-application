from typing import Annotated

from core.models import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.users import crud
from api.api_v1.users.schemas import CreateUser

router = APIRouter(tags=["Users"])

@router.post("/create", response_model=CreateUser)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_params: CreateUser
) -> CreateUser:
    return await crud.create_user(
        session=session,
        user_params=user_params
    )



