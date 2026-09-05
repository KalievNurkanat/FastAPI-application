from typing import Annotated

from api.api_v1.users.schemas import ReadUser
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth import utils as auth_utils
from auth.validation import get_active_current_auth_user, validate_auth_user

router = APIRouter(tags=["Auth"])


class TokenInfo(BaseModel):
    access_token: str
    token_type: str

    
@router.post("/login", response_model=TokenInfo)
def auth_issue_jwt(
    user: Annotated[ReadUser, Depends(validate_auth_user)]
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )


@router.get("/user/me")
def auth_user_info(
    user: Annotated[ReadUser, Depends(get_active_current_auth_user)]
):
    return {
        "User": user.username,
        "Email": user.email
    }