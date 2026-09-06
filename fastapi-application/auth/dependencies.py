from typing import Annotated

from core.models import User, db_helper
from fastapi import Depends, Form, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import utils as auth_utils
from auth.helpers import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from auth.schemas import UserSchema
from auth.validations import check_auth_user, validate_token_type

http_bearer = HTTPBearer()


async def validate_auth_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        username: str = Form(),
        password: str = Form()
):
    error_handler = HTTPException(
        status_code=401,
        detail="User not found"
    )
    stmt = select(User).where(User.username==username)
    result = await session.scalar(stmt)

    if not result:
        raise error_handler

    if not auth_utils.validate_password(
        password,
        hashed_password=result.password 
    ):
        raise error_handler

    return result


def get_current_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]
):
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {e}"           
        )
    return payload


async def get_current_auth_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    payload: Annotated[str, Depends(get_current_token_payload)]
):
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return await check_auth_user(session, payload)


async def get_current_auth_user_refresh(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    payload: Annotated[str, Depends(get_current_token_payload)]
):
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return await check_auth_user(session, payload)
    

def get_active_current_auth_user(
    user: Annotated[UserSchema, Depends(get_current_auth_user)]
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=401,
        detail="User is inactive"
    )