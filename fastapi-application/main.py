import uvicorn
from api import router as api_router
from auth import router as auth_router
from core.config import settings
from create_fastapi_app import create_app

main_app = create_app()

main_app.include_router(
    api_router,
)

main_app.include_router(
    api_router,
    prefix=settings.api.prefix
)

main_app.include_router(
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
