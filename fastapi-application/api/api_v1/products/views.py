from typing import Annotated

from core.models.db_helper import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.products import crud
from api.api_v1.products.dependencies import get_product_by_id
from api.api_v1.products.schemas import (
    CreateProduct,
    UpdateProduct,
)
from api.api_v1.products.schemas import (
    Product as sch_product,
)

router = APIRouter(
    tags=["Product"]
)


@router.get("/", response_model=list[sch_product])
async def get_products(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[sch_product]:
    return await crud.get_products(
        session
    )


@router.post("/create", response_model=CreateProduct)
async def create_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: CreateProduct
) -> CreateProduct:
    return await crud.create_product(
        session, 
        product
    )


@router.put("/update", response_model=UpdateProduct)
async def put_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: Annotated[sch_product, Depends(get_product_by_id)],
        put_product: UpdateProduct,
) -> sch_product:
    return await crud.put_product(
            session, 
            product,
            put_product
        )
    

@router.patch("/partial-update", response_model=UpdateProduct)
async def patch_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: Annotated[sch_product, Depends(get_product_by_id)],
        patch_product: UpdateProduct,
) -> sch_product:
    return await crud.patch_product(
        session,
        product,
        patch_product
    )


@router.delete("/delete", status_code=404)
async def delete_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: Annotated[sch_product, Depends(get_product_by_id)],
) -> str:
    return await crud.delete_product(
        session,
        product
    )


