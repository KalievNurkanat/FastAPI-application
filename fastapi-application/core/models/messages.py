from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class Message(Base):
    conversation_id: Mapped[int]
    role: Mapped[str]
    message: Mapped[str]
    