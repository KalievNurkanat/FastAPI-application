from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    question: str = Field(
        max_length=150,
        min_length=3
    )


class AIResponse(BaseModel):
    response: str