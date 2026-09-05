from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class User(Base):
    username: Mapped[str] = mapped_column(
        nullable=False, 
        unique=True
    )
    password: Mapped[str] = mapped_column(
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        unique=True
    )
    is_active: Mapped[bool] = mapped_column(
        default=True
    )
