from fastapi import APIRouter, Depends

from api.ai_model import gemini_assistant, gemini_chat
from api.ai_model.pydantic import AIChatResponse, AIRequest, AIResponse, UserRequest
from auth.dependencies import get_active_current_auth_user
from core.models.users import User

router = APIRouter(
    tags=["AI"]
)


@router.post("/ask", response_model=AIResponse)
async def generate_answer(request: AIRequest) -> str:
    return await gemini_assistant.generate_answer(request.question)


@router.post("/chat", response_model=AIChatResponse)
async def generate_chat(
    request: UserRequest,
    user: User = Depends(get_active_current_auth_user),
) -> str:
    return await gemini_chat.gemini_chat(
        request=request.prompt,
        user=user
    )
    
    
