from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.jwt_private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_lifetime,
        expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp = expire,
        iat = now
    )
    encoded = jwt.encode(
        to_encode,
        key=private_key,
        algorithm=algorithm
    )

    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.jwt_public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    decoded = jwt.decode(
        token,
        key=public_key,
        algorithms=[algorithm]
    )

    return decoded


def hash_password(
        password: str
) -> bytes:
    user_password: bytes = password.encode()
    salt = bcrypt.gensalt()
    pwd_hash = bcrypt.hashpw(
        user_password,
        salt
    )
    return pwd_hash.decode()


def validate_password(
        password: str,
        hashed_password: str
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode()
    )