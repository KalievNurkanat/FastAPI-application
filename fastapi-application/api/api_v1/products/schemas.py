from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseProduct(BaseModel):
    model_config = ConfigDict(
        strict=True,
    )

    title: str = Field(
        max_length=55
    )
    price: float = Field(
        gt=0,
    )
    description: str = Field(
        max_length=250
    )
    category_id: int
    register_date: datetime

