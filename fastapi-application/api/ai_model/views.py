from fastapi import APIRouter

from api.ai_model import gemini_part
from api.ai_model.pydantic import AIRequest, AIResponse

router = APIRouter(
    tags=["AI"]
)


@router.post("/ask", response_model=AIResponse)
async def generate_answer(request: AIRequest) -> str:
    return await gemini_part.generate_answer(request.question)
    
    
