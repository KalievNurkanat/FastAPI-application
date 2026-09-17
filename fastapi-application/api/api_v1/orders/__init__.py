from core.config import settings
from fastapi import APIRouter

from api.api_v1.orders.views import router as order_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    order_router,
    prefix="/order"
)