from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class APIV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"


class APIPrefix(BaseModel):
    prefix: str = "/api"
    v1: APIV1Prefix = APIV1Prefix()


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


settings = Settings()