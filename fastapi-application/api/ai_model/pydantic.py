from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    question: str = Field(
        max_length=150,
        min_length=3
    )


class AIResponse(BaseModel):
    response: str


class User(BaseModel):
    you: str = Field(
        max_length=200,
        min_length=2
    )


class AIChatResponse(BaseModel):
    AI: str