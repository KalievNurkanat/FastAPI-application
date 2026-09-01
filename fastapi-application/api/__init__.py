from fastapi import APIRouter

from api.api_v1 import router as user_v1_router

router = APIRouter()

router.include_router(router=user_v1_router)
