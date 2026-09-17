from typing import Annotated

from core.models.db_helper import db_helper
from core.models.products import Product
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_product_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product_id: int
):
    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="The product not found"
        )
    return product