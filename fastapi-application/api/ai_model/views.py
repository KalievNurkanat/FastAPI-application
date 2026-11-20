from auth.dependencies import get_active_current_auth_user
from core.models.users import User
from fastapi import APIRouter, Depends

from api.ai_model import gemini_chat
from api.ai_model.pydantic import AIChatResponse, UserRequest

router = APIRouter(
    tags=["AI"]
)


@router.post("/chat", response_model=AIChatResponse)
async def generate_chat(
    request: UserRequest,
    user: User = Depends(get_active_current_auth_user),
) -> str:
    return await gemini_chat.gemini_chat(
        request=request.prompt,
        user=user
    )
    
    
