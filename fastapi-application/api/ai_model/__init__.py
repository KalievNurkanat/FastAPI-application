from core.config import settings
from fastapi import APIRouter

from api.ai_model.views import router as ai_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(
    ai_router,
    prefix="/ai"
)