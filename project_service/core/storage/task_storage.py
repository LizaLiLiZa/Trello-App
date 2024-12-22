from .base import BaseStorage
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.tasks.requests import TaskRequest
from ..models.tasks.responses import TaskResponse

class TaskStorage(BaseStorage):
    async def get_task(self, id_state: int) -> list[TaskResponse]:
        stmt = text("""
            select * from tasks where id_state = :id_state
        """)

        params = {"id_state": id_state}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchall()
            return [
                TaskResponse(
                    id=i.id,
                    id_state=i.id_state,
                    id_low_task=i.id_low_task,
                    name=i.name,
                    description=i.description,
                    date_created=i.date_created
                )
                for i in data
            ]

    async def create_task(self, task: TaskRequest) -> int:
        stmt = text("""
            insert into tasks (id_state, id_low_task, name, description, date_created)
            values(:id_state, :id_low_task, :name, :description, :date_created)
            returning id
        """)

        params = task.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            return data.id

    async def update_task(self, task: TaskResponse) -> TaskResponse:
        stmt = text("""
            update tasks set id_state = :id_state, id_low_task = :id_low_task, name = :name, description = :description
            where id = :id
        """)

        stmt_select = text("""
            select * from tasks where id = :id
        """)

        params = task.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            data = (await session.execute(stmt_select, params)).fetchone()
            return TaskResponse(
                    id=data.id,
                    id_state=data.id_state,
                    id_low_task=data.id_low_task,
                    name=data.name,
                    description=data.description,
                    date_created=data.date_created
                )
