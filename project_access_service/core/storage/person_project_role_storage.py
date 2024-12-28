from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseStorage

from ..models.person_project_role.request import PersonProjectRolesRequest

from ..models.person_project_role.response import PersonProjectRolesResponse

class PersonProjectRoleStorage(BaseStorage):
    async def get_person_project_role_id(self, id_: int) -> PersonProjectRolesResponse:
        stmt = text("""
            select * from persons_projects_roles where id = :id_
        """)

        params = {"id_": id_}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchall()
            return PersonProjectRolesResponse(
                id=data.id,
                id_person_project=data.id_person_project,
                id_role=data.id_role
            )

    async def get_person_project_role_id_role(self, id_role: int) -> list[PersonProjectRolesResponse]:
        stmt = text("""
            select * from persons_projects_roles where id_role = :id_role
        """)

        params = {"id_role": id_role}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchall()
            return [PersonProjectRolesResponse(
                id=i.id,
                id_person_project=i.id_person_project,
                id_role=i.id_role
            )
                for i in data
            ]

    async def get_person_project_role(self, id_person_project: int) -> list[PersonProjectRolesResponse]:
        stmt = text("""
            select * from persons_projects_roles where id_person_project = :id_person_project
        """)

        params = {"id_person_project": id_person_project}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchall()
            return [PersonProjectRolesResponse(
                id=i.id,
                id_person_project=i.id_person_project,
                id_role=i.id_role
            )
                for i in data
            ]

    async def create_person_project_role(self, person_project_role: PersonProjectRolesRequest) -> int:
        stmt = text("""
            insert into persons_projects_roles (id_person_project, id_role)
            values(:id_person_project, :id_role)
            returning id
        """)

        params = person_project_role.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            return data.id

    async def delete_person_project_role_by_role(self, id_role: int) -> bool:
        stmt = text("""
            delete from persons_projects_roles where id_role = :id_role
        """)

        params = {"id_role": id_role}

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return True

    async def delete_person_project_role_by_id(self, id_: int) -> bool:
        stmt = text("""
            delete from persons_projects_roles where id = :id
        """)

        params = {"id": id_}

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return True

    async def delete_person_project_role_by_person_project(self, id_person_project: int) -> bool:
        stmt = text("""
            delete from persons_projects_roles where id_person_project = :id_person_project
        """)

        params = {"id_person_project": id_person_project}

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return True

