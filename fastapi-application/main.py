from contextlib import asynccontextmanager

import uvicorn
from api import router as api_router
from auth import router as auth_router
from core.config import settings
from core.models.db_helper import db_helper
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix
    )
    yield
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan
)
app.include_router(
    api_router,
    prefix=settings.api.prefix
)
app.include_router(
    auth_router,
    prefix=settings.api.prefix
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
