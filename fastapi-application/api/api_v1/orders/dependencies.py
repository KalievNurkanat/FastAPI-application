from typing import Annotated

from core.models.db_helper import db_helper
from core.models.orders import Order
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_order_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order_id: int
):
    order = await session.get(Order, order_id)
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="The order not found"
        )
    return order
    