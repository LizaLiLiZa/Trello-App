from .base import BaseStorage
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..models.tasks.requests import TaskCategoriesRequest
from ..models.tasks.responses import TaskCategoriesResponse

class TaskCategoriesStorage(BaseStorage):
    async def get_categories_by_id_project(self, id_project: int) -> list[TaskCategoriesResponse]:
        stmt = text("""
            select * from tasks_categories
            where id_project = :id_project
        """)

        params = {
            "id_project": id_project
        }

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchall()
            if data is None:
                raise HTTPException(status_code=422, detail="Нет категории")
            return [TaskCategoriesResponse(
                id=i.id,
                id_project=i.id_project,
                name=i.name,
                type=i.type
            ) for i in data]

    async def get_categories(self, name: str, type_: str, id_project: int) -> TaskCategoriesResponse:
        stmt = text("""
            select * from tasks_categories
            where name = :name and type = :type_ and id_project = id_project
        """)

        params = {
            "type_": type_,
            "name": name,
            "id_project": id_project
        }

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            if data is None:
                raise HTTPException(status_code=422, detail="Нет категории")
            return TaskCategoriesResponse(
                id=data.id,
                id_project=data.id_project,
                name=data.name,
                type=data.type
            )

    async def create_categories(self, categories: TaskCategoriesRequest) -> int:
        stmt_categories = text("""
            INSERT INTO tasks_categories (id_project, name, type)
            VALUES (:id_project, :name, :type)
            returning id
        """)

        params = categories.model_dump(mode="python")

        try:
            existing_category = await self.get_categories(
                categories.name, categories.type, categories.id_project
            )

            if existing_category:
                raise HTTPException(status_code=422, detail="Такая категория уже есть!")
        except Exception:
            async with self.get_session() as session:
                session: AsyncSession
                data = (await session.execute(stmt_categories, params)).fetchone()
                await session.commit()
                return data.id

    async def update_categories(self, categories: TaskCategoriesResponse) -> TaskCategoriesResponse:
        stmt = text("""
            update tasks_categories set name = :name where id = :id
        """)

        params = categories.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return await self.get_categories(categories.name, categories.type, categories.id_project)
