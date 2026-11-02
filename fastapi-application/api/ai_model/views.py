from fastapi import APIRouter

from api.ai_model import gemini_assistant, gemini_chat
from api.ai_model.pydantic import AIChatResponse, AIRequest, AIResponse, User

router = APIRouter(
    tags=["AI"]
)


@router.post("/ask", response_model=AIResponse)
async def generate_answer(request: AIRequest) -> str:
    return await gemini_assistant.generate_answer(request.question)


@router.post("/chat", response_model=AIChatResponse)
async def generate_chat(user: User) -> str:
    return await gemini_chat.gemini_chat(user.you)
    
    
