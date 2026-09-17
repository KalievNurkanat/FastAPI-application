from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from core.models.association_tables import OrderProduct
    from core.models.products import Product


class Order(Base):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc)
    )
    promocode: Mapped[str | None]
    products: Mapped[list["Product"]] = relationship(
        secondary="order_product_association",
        back_populates="orders",
        overlaps="order_details"
    )
    product_details: Mapped[list["OrderProduct"]] = relationship(
        back_populates="order",
        overlaps="orders, products"
    )


