from typing import Annotated

from core.models.db_helper import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.categories import crud
from api.api_v1.categories.dependencies import get_category_by_id
from api.api_v1.categories.schemas import (
    Category as sch_category,
)
from api.api_v1.categories.schemas import (
    CreateCategory,
    UpdateCategory,
)

router = APIRouter(
    tags=["Category"]
)


@router.get("/", response_model=list[sch_category])
async def get_categories(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[sch_category]:
    return await crud.get_categories(
        session
    )


@router.post("/create", response_model=CreateCategory)
async def create_category(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        category: CreateCategory
) -> CreateCategory:
    return await crud.create_category(
        session, 
        category
    )


@router.put("/update", response_model=UpdateCategory)
async def put_category(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        category: Annotated[sch_category, Depends(get_category_by_id)],
        put_category: UpdateCategory,
) -> sch_category:
    return await crud.put_category(
            session, 
            category,
            put_category
        )
    

@router.patch("/partial-update", response_model=UpdateCategory)
async def patch_category(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        category: Annotated[sch_category, Depends(get_category_by_id)],
        patch_category: UpdateCategory,
) -> sch_category:
    return await crud.patch_category(
        session,
        category,
        patch_category
    )


@router.delete("/delete", status_code=404)
async def delete_category(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        category: Annotated[sch_category, Depends(get_category_by_id)],
) -> str:
    return await crud.delete_category(
        session,
        category
    )



