from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseStorage

from ..models.access_right.request import AccessRightsRequest

from ..models.access_right.response import AccessRightsResponse

class AccessRightStorage(BaseStorage):
    async def get_access_right(self) -> list[AccessRightsResponse]:
        stmt = text("""
            select * from access_rights
        """)

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt)).fetchall()
            return [AccessRightsResponse(
                id=i.id,
                date_created=i.date_created,
                name=i.name
            )
                for i in data
            ]

    async def create_access_right(self, access_right: AccessRightsRequest) -> int:
        stmt = text("""
            insert into access_rights (date_created, name)
            values(:date_created, :name)
            returning id
        """)

        params = access_right.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            return data.id
        
    async def delete_acces_right(self, id_: int) -> bool:
        stmt = text("""
            delete from access_rights where id = :id
        """)

        params = {"id": id_}

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return True
