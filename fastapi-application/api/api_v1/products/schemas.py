from pydantic import BaseModel, ConfigDict, Field


class BaseProduct(BaseModel):
    title: str = Field(
        ge=1,
        le=35
    )
    price: int = Field(
        gt=0,
    )
    description: str = Field(
        gt=0,
        le=250
    )
    category_id: int
    register_date: 
