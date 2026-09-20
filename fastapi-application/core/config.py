import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class APIV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"


class APIPrefix(BaseModel):
    prefix: str = "/api"
    v1: APIV1Prefix = APIV1Prefix()


class LoggingConfig(BaseModel):
    log_levels: Literal [
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_value.upper()]


class AuthJWT(BaseModel):
    jwt_private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    jwt_public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_lifetime: int = 3
    refresh_token_lifetime: int = 35


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_conventions: dict[str,str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class RedisDB(BaseModel):
    cache: int = 0


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: RedisDB = RedisDB()


class CacheNameSpaces(BaseModel):
    users_list: str = "users-list"


class CacheConfig(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNameSpaces = CacheNameSpaces()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__"
    )
    run: RunConfig = RunConfig()
    api: APIPrefix = APIPrefix()
    db: DataBaseConfig
    auth_jwt: AuthJWT = AuthJWT()
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()