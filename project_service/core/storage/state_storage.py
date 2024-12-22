from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from .base import BaseStorage

from ..models.states.request import StateRequest
from ..models.states.response import StateResponse

class StateStorage(BaseStorage):
    async def create_state(self, state: StateRequest) -> list[StateResponse]:
        stmt = text("""
            insert into states (id_board, name, date_created)
            values(:id_board, :name, :date_created)
        """)

        stmt_select = text("""
            select * from states where id_board = :id_board
        """)

        params = state.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession

            await session.execute(stmt, params)
            await session.commit()

            d = (await session.execute(stmt_select, params)).fetchall()

            return [
                StateResponse(
                    id= i.id,
                    id_board = i.id_board,
                    name = i.name,
                    date_created = i.date_created
                )
                for i in d
            ]

    async def get_states(self, id_board: int) -> list[StateResponse]:
        stmt = text("""
            select * from states where id_board = :id_board
        """)

        params = {"id_board": id_board}

        async with self.get_session() as session:
            session: AsyncSession

            d = (await session.execute(stmt, params)).fetchall()
            if d == []:
                raise HTTPException(status_code=422, detail="У данного проекта нет состояний")

            return [
                StateResponse(
                    id= i.id,
                    id_board = i.id_board,
                    name = i.name,
                    date_created = i.date_created
                )
                for i in d
            ]

    async def update_states(self, state: StateRequest) -> list[StateResponse]:
        stmt = text("""
            update states set name = :name where id = :id
        """)

        params = state.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession

            await session.execute(stmt, params)
            await session.commit()
            return await self.get_states(state.id_board)
