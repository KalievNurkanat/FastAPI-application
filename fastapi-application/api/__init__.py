from fastapi import APIRouter

from api.api_v1 import router as v1_routers

router = APIRouter()

router.include_router(router=v1_routers)
