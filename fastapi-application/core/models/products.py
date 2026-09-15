from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from core.models.association_tables import OrderProduct
    from core.models.orders import Order


class Category(Base):
    __tablename__ = "categories"
    title: Mapped[str]


class Product(Base):
    title: Mapped[str] = String(35)
    price: Mapped[float]
    description: Mapped[int] = String(120)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )
    register_date: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now(timezone.utc)
    )
    orders: Mapped[list["Order"]] = relationship(
        secondary="order_product_association",
        back_populates="products",
        overlaps="product_details"
    )
    order_details: Mapped[list["OrderProduct"]] = relationship(
            back_populates="product",
            overlaps="orders, products"
        )

    __table_args__ = (
        CheckConstraint(
            "price > 0", 
            name="price"
        )
    )

