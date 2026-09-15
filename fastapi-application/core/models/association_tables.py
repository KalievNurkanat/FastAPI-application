from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.orders import Order
    from core.models.products import Product


class OrderProduct(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint(
        "order_id", "product_id"
    ),
        CheckConstraint(
            "count <= 20",
            name="count"
        )
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )
    count: Mapped[int] = mapped_column(
        server_default="1",
        default=1
    )
    order: Mapped["Order"] = relationship(
        back_populates="product_details",
        overlaps="order, product"
    )
    product: Mapped["Product"] = relationship(
        back_populates="order_details",
        overlaps="order, product"
    )



