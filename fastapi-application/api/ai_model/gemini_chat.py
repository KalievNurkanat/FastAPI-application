from core.config import settings
from google import genai
from google.genai import types

from api.ai_model.gemini_needs import get_product
from api.ai_model.pydantic import AIChatResponse, User

client = genai.Client(api_key=settings.gemini.api_key)

async def gemini_chat(
    user: User,
) -> AIChatResponse:
    chat = client.aio.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            tools=[get_product]
        )
    )
    user_message = user
    response = await chat.send_message(user_message) 
    
    return {"AI": response.text}


