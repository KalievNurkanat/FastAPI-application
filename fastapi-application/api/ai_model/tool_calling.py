from core.models.db_helper import db_helper
from core.models.products import Product
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_products(
    session: AsyncSession,
) -> list[dict]:

    result = await session.execute(
        select(Product)
    )

    products = result.scalars().all()

    return [
        {
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "description": product.description
        }
        for product in products
    ]


async def get_product() -> list[dict]:
    async with db_helper.session_factory() as session:
        return await fetch_products(session)


