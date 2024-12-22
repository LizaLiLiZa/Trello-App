from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from .base import BaseStorage

from ..models.project.request import CreateProjectRequest
from ..models.project.response import ProjectResponse
from ..models.project.request import UpdateProjectRequest

class ProjectStorage(BaseStorage):
    async def create_project(self, project: CreateProjectRequest) -> list[ProjectResponse]:
        stmt = text("""
            insert into projects (id_person, name, description, date_created)
            values(:id_person, :name, :description, :date_created)
        """)

        stmt_select = text("""
            select * from projects where id_person = :id_person and date_created = :date_created
        """)

        async with self.get_session() as session:
            session: AsyncSession

            params = project.model_dump(mode="python")

            await session.execute(stmt, params)
            await session.commit()

            d = (await session.execute(stmt_select, params)).fetchall()
            return [ProjectResponse(
                id = i.id,
                id_person = i.id_person,
                name = i.name,
                description = i.description,
                date_created = i.date_created
            ) for i in d]

    async def get_project(self, id_person: int) -> list[ProjectResponse]:
        stmt = text("""
            select * from projects where id_person = :id
        """)

        async with self.get_session() as session:
            session: AsyncSession
            params = {
                "id": id_person
            }

            d = (await session.execute(stmt, params)).fetchall()

            if d == []:
                raise HTTPException(status_code=422, detail="У этого пользователя нет проектов.")

            return [ProjectResponse(
                id = i.id,
                id_person = i.id_person,
                name = i.name,
                description = i.description,
                date_created = i.date_created
            ) for i in d]

    async def update_project(self, project: UpdateProjectRequest) -> ProjectResponse:
        stmt = text("""
            update projects set name = :name, description = :description
            where id = :id
        """)

        stmt_selection = text("""
            select * from projects where id = :id
            limit 1
        """)

        params = project.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession

            await session.execute(stmt, params)
            await session.commit()

            d = (await session.execute(stmt_selection, params)).fetchone()
            return ProjectResponse(
                id = d.id,
                id_person = d.id_person,
                name = d.name,
                description = d.description,
                date_created = d.date_created
            )

    async def delete_project(self, id_project: int) -> bool:
        stmt = text("""
            delete from projects where id = :id
        """)

        stmt_select = text("""
            select * from projects where id = :id
        """)

        params = {
            "id": id_project
        }

        async with self.get_session() as session:
            session: AsyncSession
            d = (await session.execute(stmt_select, params)).fetchone()
            if d is None:
                raise HTTPException(status_code=422, detail="Не найден проект с таким id")

            await session.execute(stmt, params)
            await session.commit()
            return True
