from sqlalchemy import text
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseStorage
from ..models.boards.requests import BoardRequest
from ..models.boards.responses import BoardResponse

class BoardStorage(BaseStorage):
    async def get_board_by_id(self, id_board: int) -> BoardResponse:
        stmt = text("""
            select * from boards where id = :id
        """)

        params = {"id": id_board}
        async with self.get_session() as session:
            session:AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            if data is None:
                raise HTTPException(status_code=422, detail="Нет такой доски!")
            return BoardResponse(
                id=data.id,
                id_project=data.id_project,
                name = data.name,
                description = data.description,
                date_created=data.date_created
            )

    async def get_board(self, id_project: int) -> list[BoardResponse]:
        stmt = text("""
            select * from boards where id_project = :id_project
        """)

        params = {"id_project": id_project}

        async with self.get_session() as session:
            session: AsyncSession
            all_data = (await session.execute(stmt, params)).fetchall()
            return [BoardResponse(
                id=data.id,
                id_project=data.id_project,
                name = data.name,
                description = data.description,
                date_created=data.date_created
            ) for data in all_data]

    async def create_board(self, board: BoardRequest) -> list[BoardResponse]:
        stmt = text("""
            insert into boards (id_project, name, description, date_created)
            values(:id_project, :name, :description, :date_created)
        """)

        params = board.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return await self.get_board(board.id_project)

    async def update_board(self, board: BoardResponse) -> BoardResponse:
        stmt = text("""
            update boards set name = :name, description = :description
            where id = :id
        """)

        params = board.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return await self.get_board_by_id(board.id)
