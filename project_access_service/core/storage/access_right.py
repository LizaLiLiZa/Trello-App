from datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseStorage

class AccessRightStorage(BaseStorage):
    async def create_access_right(self):
        stmt = text("""
            insert into  set ()
        """)
