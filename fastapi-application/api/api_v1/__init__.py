from fastapi import APIRouter

from api.api_v1.categories import router as category_router
from api.api_v1.products import router as product_router
from api.api_v1.users import router as users_router

router = APIRouter()

router.include_router(users_router)
router.include_router(category_router)
router.include_router(product_router)