from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class BaseOrder(BaseModel):
    promocode: str | None = None
    created_at: datetime | None


class Order(BaseOrder):
    id: int


class ReadOrder(BaseOrder):
    pass


class CreateOrder(BaseOrder):
    product_details: list[SetProductForOrder]
    

class ProductID(BaseModel):
    id: int


class SetProductForOrder(BaseModel):
    count: int
    product: ProductID


class UpdateOrder(BaseOrder):
    pass


class DeleteOrder(BaseOrder):
    pass