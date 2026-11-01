from fastapi import APIRouter

from api.ai_model import router as ai_router
from api.api_v1 import router as api_v1_routers

router = APIRouter()

router.include_router(
    router = api_v1_routers,
)
router.include_router(
    router=ai_router
)
