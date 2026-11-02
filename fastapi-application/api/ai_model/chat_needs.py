from core.models.db_helper import db_helper
from core.models.messages import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_messages(
    session: AsyncSession
) -> list[dict]:
    result = await session.execute(
        select(Message)
    )   
    messages = result.scalars().all()

    return [
        {
            "conversation_id": message.conversation_id,
            "role": message.role,
            "message": message.message
        }
        for message in messages
    ]

async def get_messages() -> list[dict]:
    async with db_helper.session_factory() as session:
        return await fetch_messages(session)


async def create_messages(
    session: AsyncSession,
    conversation_id: int,
    role: str,
    message: str
):
    message_in = Message(
        conversation_id=conversation_id,
        role=role,
        message=message
    )
    session.add(message_in)
    await session.commit()
    await session.refresh(message_in)

    return message_in


async def create_message(
    conversation_id: int,
    role: str,
    message: str
):
    async with db_helper.session_factory() as session:
        return await create_messages(
            session,
            conversation_id,
            role,
            message
        )