from fastapi import APIRouter

from api.api_v1.users import router as users_router

router = APIRouter()

router.include_router(users_router)