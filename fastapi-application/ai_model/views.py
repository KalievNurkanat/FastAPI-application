from fastapi import APIRouter

from ai_model import gemini_part
from ai_model.pydantic import AIRequest, AIResponse

router = APIRouter(
    tags=["AI"]
)


@router.post("/ask", response_model=AIResponse)
async def generate_answer(request: AIRequest) -> str:
    return await gemini_part.generate_answer(request.question)
    
    
