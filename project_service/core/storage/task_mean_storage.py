from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .base import BaseStorage

from ..models.tasks.requests import TaskTextRequest
from ..models.tasks.requests import TaskDateRequest
from ..models.tasks.requests import TaskPersonRequest
from ..models.tasks.requests import TaskMeanRequest
from ..models.tasks.requests import TaskMeanUpdateRequest

from ..models.tasks.responses import TaskTextResponse
from ..models.tasks.responses import TaskMeanTextResponse
from ..models.tasks.responses import TaskTextCategoriesResponse
from ..models.tasks.responses import TaskMeanResponse
from ..models.tasks.responses import TaskDateCategoriesResponse
from ..models.tasks.responses import TaskMeanDateResponse
from ..models.tasks.responses import TaskPersonCategoriesResponse
from ..models.tasks.responses import TaskMeanPersonResponse

class TaskMeanStorage(BaseStorage):
    async def get_task_mean_text(self, id_task: int) -> TaskMeanTextResponse:
        stmt = text("""
            select 
                tasks_means.id as mean_id,
                tasks_means.id_task_categories as mean_task_categories_id,
                tasks_text.id as text_id,
                tasks_categories.id as category_id,
                tasks_text.text as text_content,
                tasks_categories.name as category_name
            from tasks_means
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
                data=[
                    TaskTextCategoriesResponse(
                        id=i.mean_id,
                        id_text=i.text_id,
                        id_task_categories=i.category_id,
                        text_=i.text_content,
                        name=i.category_name
                    )
                    for i in data_
                ]
            )

    async def get_task_mean_date(self, id_task: int) -> TaskMeanTextResponse:
        stmt = text("""
            select 
                tasks_means.id as mean_id,
                tasks_means.id_task_categories as mean_task_categories_id,
                tasks_date.id as date_id,
                tasks_categories.id as category_id,
                tasks_date.date as date_content,
                tasks_categories.name as category_name
            from tasks_means
            join tasks_date on tasks_means.id_mean = tasks_date.id
            join tasks_categories on tasks_categories.id = tasks_means.id_task_categories
            where tasks_means.id_task = :id_task
        """)

        params = {"id_task": id_task}

        async with self.get_session() as session:
            session: AsyncSession
            data_ = (await session.execute(stmt, params)).fetchall()

            return TaskMeanDateResponse(
                id_task=id_task,
                data=[
                    TaskDateCategoriesResponse(
                        id=i.mean_id,
                        id_date=i.date_id,
                        id_task_categories=i.category_id,
                        date_=i.date_content,
                        name=i.category_name
                    )
                    for i in data_
                ]
            )

    async def get_task_mean_person(self, id_task: int) -> TaskPersonCategoriesResponse:
        stmt = text("""
            select 
                tasks_means.id as mean_id,
                tasks_means.id_task_categories as mean_task_categories_id,
                tasks_person.id as person_id,
                tasks_categories.id as category_id,
                tasks_person.id_person as person_content,
                tasks_categories.name as category_name
            from tasks_means
            join tasks_person on tasks_means.id_mean = tasks_person.id
            join tasks_categories on tasks_categories.id = tasks_means.id_task_categories
            where tasks_means.id_task = :id_task
        """)

        params = {"id_task": id_task}

        async with self.get_session() as session:
            session: AsyncSession
            data_ = (await session.execute(stmt, params)).fetchall()

            return TaskMeanPersonResponse(
                id_task=id_task,
                data=[
                    TaskPersonCategoriesResponse(
                        id=i.mean_id,
                        id_person=i.person_id,
                        id_task_categories=i.category_id,
                        person_=i.person_content,
                        name=i.category_name
                    )
                    for i in data_
                ]
            )

    async def create_task_mean(self, task_mean: TaskMeanRequest) -> int:
        stmt = text("""
            insert into tasks_means (id_task_categories, id_mean, id_task)
            values(:id_task_categories, :id_mean, :id_task)
            returning id
        """)

        params = task_mean.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            return data.id

    async def update_task_mean(self, task_mean: TaskMeanUpdateRequest) -> TaskMeanResponse:
        stmt = text("""
            update from tasks_mean set id_mean = :id_mean
            where id = :id
        """)

        stmt_select = text("""
            select * from tasks_mean where id = :id
        """)

        params = task_mean.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            data = (await session.execute(stmt_select, params)).fetchone()
            return TaskMeanResponse(
                id = data.id,
                id_task=data.id_task,
                id_mean=data.id_mean,
                id_task_categories=data.id_task_categories
            )

    async def delete_task_mean(self, id_: int) -> bool:
        stmt = text("""
            delete from tasks_mean where id = :id
        """)

        params = {"id": id_}

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return True

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
