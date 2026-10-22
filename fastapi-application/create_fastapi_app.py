from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from core.config import settings
from core.models import db_helper
from error_handlers import register_error_handlers
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from middlewares.middlewares import register_middlewares
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )

    yield
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=JSONResponse
    )
    register_error_handlers(app)
    register_middlewares(app)

    return app