from core.config import settings
from fastapi import APIRouter

from auth.jwt_auth import router as auth_routers

router = APIRouter(    
    prefix=settings.api.v1.prefix
)

router.include_router(router=auth_routers)
