from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .base import BaseStorage

from ..models.tasks.requests import TaskTextRequest
from ..models.tasks.requests import TaskDateRequest
from ..models.tasks.requests import TaskPersonRequest

from ..models.tasks.responses import TaskTextResponse
from ..models.tasks.responses import TaskMeanTextResponse
from ..models.tasks.responses import TaskTextCategoriesResponse


class TaskMeanStorage(BaseStorage):
    async def get_task_mean_text(self, id_task: int) -> TaskMeanTextResponse:
        stmt = text("""
            select * from tasks_means
            join tasks_text on tasks_means.id_mean = tasks_text.id
            join tasks_categories on tasks_categories.id = tasks_means.id_task_categories
            where tasks_means.id_task = :id_task
        """)

        params = {"id_task": id_task}

        async with self.get_session() as session:
            session: AsyncSession
            data_ = (await session.execute(stmt, params)).fetchall()
            return TaskMeanTextResponse(
                id_task=id_task,
                data=[TaskTextCategoriesResponse(
                    id=i.tasks_means.id,
                    id_text=i.tasks_text.id,
                    id_task_categories=i.tasks_categories.id,
                    text_=i.tasks_text.text,
                    name=i.tasks_categories.name
                )
                    for i in data_
                ]
            )

    async def get_text(self, id_task_categories: int) -> list[TaskTextResponse]:
        stmt_text = text("""
            select * from tasks_text where id_task_categories = :id_task_categories
        """)

        params = {"id_task_categories": id_task_categories}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt_text, params)).fetchall()
            if data == []:
                raise HTTPException(status_code=422, detail="Нет значений у этой категории!")
            return [TaskTextResponse(
                id=i.id,
                id_task_categories=i.id_task_categories,
                text=i.text
            )
            for i in data]

    async def create_text(self, text_: TaskTextRequest) -> int:
        stmt = text("""
            insert into tasks_text (text, id_task_categories)
            values(:text, :id_task_categories)
            returning id
        """)

        stmt_select = text("""
            select * from tasks_text
            where text = :text and id_task_categories = :id_task_categories
        """)

        params = text_.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt_select, params)).fetchone()
            if not (data is None):
                raise HTTPException(status_code=422, detail="Такое значение уже существует.")
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            return data.id

    async def create_date(self, date: TaskDateRequest) -> int:
        stmt = text("""
            insert into tasks_date (date, id_task_categories)
            values(:date, :id_task_categories)
            returning id
        """)

        params = date.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            return data.id
        return False

    async def create_person(self, person: TaskPersonRequest) -> int:
        stmt = text("""
            insert into tasks_person (id_person, id_task_categories)
            values(:id_person, :id_task_categories)
            returning id
        """)

        params = person.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            return data.id

    async def delete_text(self, id_: int) -> bool:
        stmt = text("""
            delete from tasks_text where id = :id
        """)

        params = {"id": id_}

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return True

    async def delete_date(self, id_: int) -> bool:
        stmt = text("""
            delete from tasks_date where id = :id
        """)

        params = {"id": id_}

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return True

    async def delete_person(self, id_: int) -> bool:
        stmt = text("""
            delete from tasks_person where id = :id
        """)

        params = {"id": id_}

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return True
