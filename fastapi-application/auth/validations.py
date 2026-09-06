from typing import Annotated

from core.models import User, db_helper
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.helpers import TOKEN_TYPE_FIELD


def validate_token_type(
        payload: dict,
        type: str
):
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != type:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token type {token_type}, expected {type}"
        )
    return True


async def check_auth_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    payload: dict   
):
    username: str | None = payload.get("username") 
    stmt = select(User).where(User.username==username)
    user = await session.scalar(stmt)
    if user:
        return user
    
    raise HTTPException(
            status_code=401,
            detail="Token invalid"
        ) 