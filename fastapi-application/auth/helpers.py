from datetime import timedelta

from core.config import settings

from auth import auth_utils
from auth.schemas import UserSchema

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
TOKEN_TYPE_FIELD = "type"


def create_jwt_token(
        token_data: dict,
        token_type: str,
        expire_minutes: int = settings.auth_jwt.access_token_lifetime,
        expire_timedelta: timedelta | None = None
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
    )


def create_access_token(
        user: UserSchema
) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt_token(
        token_data=jwt_payload,
        token_type=ACCESS_TOKEN_TYPE,
        expire_minutes=settings.auth_jwt.access_token_lifetime
    )


def create_refresh_token(
        user: UserSchema
) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username
    }
    return create_jwt_token(
        token_data=jwt_payload,
        token_type=REFRESH_TOKEN_TYPE ,
        expire_minutes=settings.auth_jwt.refresh_token_lifetime
    )


