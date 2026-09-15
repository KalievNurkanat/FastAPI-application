from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from core.models.products import Product


class Category(Base):
    __tablename__ = "categories"
    title: Mapped[str] = mapped_column(
        String(55)
    )
    products: Mapped[list["Product"]] = relationship(
            back_populates="category",
            overlaps="product, category"
        )