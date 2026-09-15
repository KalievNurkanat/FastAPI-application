from typing import Annotated

from core.models.categories import Category
from core.models.db_helper import db_helper
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_category_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        category_id: int
):
    category = await session.get(Category, category_id)
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="The category not found"
        )
    return category
    