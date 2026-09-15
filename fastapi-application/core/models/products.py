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
    products: Mapped[list["Product"]] = relationship(
            back_populates="category",
            overlaps="product, category"
        )


class Product(Base):
    title: Mapped[str] = mapped_column(
        String(35)
    )
    price: Mapped[float]
    description: Mapped[str] = mapped_column(
        String(250)
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )
    register_date: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now(timezone.utc)
    )
    category: Mapped[Category] = relationship(
        back_populates="products",
        overlaps="products, category"
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

