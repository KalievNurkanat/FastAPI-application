from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from core.models import Base

class User(Base, SQLAlchemyBaseUserTable[int]):

    @classmethod
    def get_db(cls, session: AsyncSession):
        return cls(SQLAlchemyUserDatabase(session, cls))

