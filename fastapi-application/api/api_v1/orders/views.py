from typing import Annotated

from core.models.db_helper import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.orders import crud
from api.api_v1.orders.dependencies import get_order_by_id
from api.api_v1.orders.schemas import (
    CreateOrder,
    UpdateOrder,
)
from api.api_v1.orders.schemas import (
    Order as sch_order,
)

router = APIRouter(
    tags=["Order"]
)


@router.get("/", response_model=list[sch_order])
async def get_orders(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[sch_order]:
    return await crud.get_orders(
        session
    )


@router.post("/create", response_model=CreateOrder)
async def create_order(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order: CreateOrder
) -> CreateOrder:
    return await crud.create_order(
        session, 
        order
    )


@router.put("/update", response_model=UpdateOrder)
async def put_order(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order: Annotated[sch_order, Depends(get_order_by_id)],
        put_order: UpdateOrder,
) -> sch_order:
    return await crud.put_order(
            session, 
            order,
            put_order
        )
    

@router.patch("/partial-update", response_model=UpdateOrder)
async def patch_order(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order: Annotated[sch_order, Depends(get_order_by_id)],
        patch_order: UpdateOrder,
) -> sch_order:
    return await crud.patch_order(
        session,
        order,
        patch_order
    )


@router.delete("/delete", status_code=404)
async def delete_order(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order: Annotated[sch_order, Depends(get_order_by_id)],
) -> str:
    return await crud.delete_order(
        session,
        order
    )



