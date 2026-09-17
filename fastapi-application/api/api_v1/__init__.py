from fastapi import APIRouter

from api.api_v1.categories import router as category_router
from api.api_v1.orders import router as order_router
from api.api_v1.products import router as product_router
from api.api_v1.users import router as users_router

router = APIRouter()

router.include_router(
    router = users_router
)
router.include_router(
    router = category_router
)
router.include_router(
    router = product_router
)
router.include_router(
    router = order_router
)