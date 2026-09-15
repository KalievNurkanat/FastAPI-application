from typing import Annotated

from core.models.categories import Category
from core.models.db_helper import db_helper
from fastapi import Depends
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.categories.schemas import (
    Category as sch_category,
)
from api.api_v1.categories.schemas import (
    CreateCategory,
    UpdateCategory,
)


async def get_categories(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[sch_category]:
    stmt = select(Category).order_by(Category.id)
    result: Result = await session.execute(stmt)
    categories = result.scalars().all()
    return categories


async def create_category(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        category: CreateCategory
) -> CreateCategory:
    category_in = Category(**category.model_dump())
    session.add(category_in)
    await session.commit()
    await session.refresh(category_in)

    return category_in


async def put_category(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        category: sch_category,
        put_category: UpdateCategory,
) -> sch_category:
    for key, value in put_category.model_dump().items():
        setattr(category, key, value)
    await session.commit()
    
    return category


async def patch_category(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        category: sch_category,
        patch_category: UpdateCategory,
) -> sch_category:
    for key, value in patch_category.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    await session.commit()
    
    return category


async def delete_category(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        category: sch_category
) -> str:
    session.delete(category)
    session.commit()
    return "The category successfully deleted"

