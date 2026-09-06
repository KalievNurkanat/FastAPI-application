from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth.dependencies import (
    UserSchema,
    get_active_current_auth_user,
    get_current_auth_user_refresh,
    validate_auth_user,
)
from auth.helpers import create_access_token, create_refresh_token

router = APIRouter(tags=["Auth"])


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None    
    type: str = "Bearer"

    
@router.post("/login", response_model=TokenInfo)
def auth_issue_jwt(
    user: Annotated[UserSchema, Depends(validate_auth_user)]
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
        "/access-token-issue",
        response_model=TokenInfo,
        response_model_exclude_none=True
        )
async def auth_access_issue_jwt(
    user: Annotated[UserSchema, Depends(get_current_auth_user_refresh)]
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token
    )


@router.get("/user/me")
def auth_user_info(
    user: Annotated[UserSchema, Depends(get_active_current_auth_user)]
):
    return {
        "User": user.username,
        "Email": user.email
    }