from core.config import settings
from google import genai

client = genai.Client(api_key=settings.gemini.api_key)

async def generate_answer(quesion: str):
    response = await client.aio.models.generate_content(
        model="gemini-3.8-flash",
        contents=quesion
    )

    if response.text is None:
        raise RuntimeError("AI get an empty query")

    return {"response": response.text}
