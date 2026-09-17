from typing import Annotated

from core.models.association_tables import OrderProduct
from core.models.db_helper import db_helper
from core.models.orders import Order
from core.models.products import Product
from fastapi import Depends, HTTPException
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.api_v1.orders.schemas import (
    CreateOrder,
    UpdateOrder,
)
from api.api_v1.orders.schemas import (
    Order as sch_order,
)
from api.api_v1.products.dependencies import get_product_by_id


async def get_orders(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[sch_order]:
    stmt = select(Order).order_by(Order.id)
    result: Result = await session.execute(stmt)
    orders = result.scalars().all()
    return orders


async def create_order(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order: CreateOrder
) -> CreateOrder:
    order_in = Order(
        promocode=order.promocode,
        created_at=order.created_at
    )
    session.add(order_in)
    for item in order.product_details:
        product = await get_product_by_id(
            session, 
            item.product.id
        )
        if product is not None:
            order_in.product_details.append(
                    OrderProduct(
                        product=product,
                        count=item.count
                    )
                )
    await session.commit()
    stmt = (
        select(Order)
        .where(Order.id==order_in.id)
        .options(selectinload(Order.product_details).selectinload(OrderProduct.product))
    )
    result = await session.scalar(stmt)

    return result
    
    


async def put_order(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order: sch_order,
        put_order: UpdateOrder,
) -> sch_order:
    for key, value in put_order.model_dump().items():
        setattr(order, key, value)
    await session.commit()
    
    return order


async def patch_order(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order: sch_order,
        patch_order: UpdateOrder,
) -> sch_order:
    for key, value in patch_order.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    await session.commit()
    
    return order


async def delete_order(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order: sch_order
) -> str:
    session.delete(order)
    session.commit()
    return "The order successfully deleted"

