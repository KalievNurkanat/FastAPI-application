from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int]

    __table_args__ = (
            CheckConstraint(
                "age >= 0",
                name="age"
            ),
        )



    