from typing import Annotated

from core.models.db_helper import db_helper
from core.models.products import Product
from fastapi import Depends
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.products.schemas import (
    CreateProduct,
    UpdateProduct,
)
from api.api_v1.products.schemas import (
    Product as sch_product,
)


async def get_products(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[sch_product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return products


async def create_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: CreateProduct
) -> CreateProduct:
    product_in = Product(**product.model_dump())
    session.add(product_in)
    await session.commit()
    await session.refresh(product_in)

    return product_in


async def put_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: sch_product,
        put_product: UpdateProduct,
) -> sch_product:
    for key, value in put_product.model_dump().items():
        setattr(product, key, value)
    await session.commit()
    
    return product


async def patch_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: sch_product,
        patch_product: UpdateProduct,
) -> sch_product:
    for key, value in patch_product.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    await session.commit()
    
    return product


async def delete_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: sch_product
) -> str:
    session.delete(product)
    session.commit()
    return "The product successfully deleted"

