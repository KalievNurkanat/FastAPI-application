from core.config import settings
from google import genai
from google.genai import types

from api.ai_model.gemini_needs import get_product

client = genai.Client(api_key=settings.gemini.api_key)

async def generate_answer(quesion: str):
    response = await client.aio.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=quesion,
        config=types.GenerateContentConfig(
            tools=[get_product]
        )
    )

    if response.text is None:
        raise RuntimeError("AI get an empty query")

    return {"response": response.text}
