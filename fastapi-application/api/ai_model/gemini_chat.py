from auth.dependencies import get_active_current_auth_user
from core.config import settings
from core.models.users import User
from fastapi import Depends
from google import genai
from google.genai import types

from api.ai_model.chat_needs import create_message, get_messages
from api.ai_model.gemini_needs import get_product
from api.ai_model.pydantic import AIChatResponse, UserRequest

client = genai.Client(api_key=settings.gemini.api_key)

async def gemini_chat(
    request: UserRequest,
    user: User = Depends(get_active_current_auth_user),
    # session: AsyncSession = Depends(db_helper.session_getter),
) -> AIChatResponse:
    history_db = await get_messages(user=user)
    history = [
        types.Content(
            role="model" if msg["role"] == "AI" else "user",
            parts=[
                types.Part.from_text(text=msg["message"])
            ]
        )
        for msg in history_db
    ]
    chat = client.aio.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(  
            tools=[get_product],
        ),
        history=history
    )
    await create_message(
        conversation_id=1,
        role="user",
        user_id=user.id,
        message=request
    )
    response = await chat.send_message(request) 
    await create_message(
        conversation_id=1,
        role="AI",
        user_id=user.id,
        message=response.text,
    )
  
    return {"AI": response.text}


