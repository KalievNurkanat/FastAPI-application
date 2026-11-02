from core.config import settings
from google import genai
from google.genai import types

from api.ai_model.chat_needs import create_message, get_messages
from api.ai_model.gemini_needs import get_product
from api.ai_model.pydantic import AIChatResponse, User

client = genai.Client(api_key=settings.gemini.api_key)

async def gemini_chat(
    user: User,
) -> AIChatResponse:
    chat = client.aio.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            tools=[get_messages, get_product]
        )
    )
    user_message = user
    await create_message(
        conversation_id=1,
        role="user",
        message=user_message
    )
    response = await chat.send_message(user_message) 
    await create_message(
        conversation_id=1,
        role="AI",
        message=response.text
    )
    
    return {"AI": response.text}


