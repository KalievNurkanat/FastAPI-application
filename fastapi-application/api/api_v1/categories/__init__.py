from core.config import settings
from fastapi import APIRouter

from api.api_v1.categories.views import router as category_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(
    category_router,
    prefix="/category"
)