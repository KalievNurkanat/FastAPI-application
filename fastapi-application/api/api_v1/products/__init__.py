from core.config import settings
from fastapi import APIRouter

from api.api_v1.products.views import router as product_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(
    product_router,
    prefix="/product"
)