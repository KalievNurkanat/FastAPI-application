from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class Message(Base):
    conversation_id: Mapped[int]
    role: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    message: Mapped[str]
    