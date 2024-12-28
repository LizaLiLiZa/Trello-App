from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseStorage

from ..models.roles.request import ProjectRolesRequest

from ..models.roles.response import ProjectRolesResponse

from database import Session
from .person_project_role_storage import PersonProjectRoleStorage

class RoleStorage(BaseStorage):
    async def get_role(self, id_: int) -> ProjectRolesResponse:
        stmt = text("""
            select * from projects_roles where id = :id_
        """)

        params = {"id_": id_}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchall()
            return ProjectRolesResponse(
                id=data.id,
                id_project=data.id_project,
                name=data.name
            )
    async def get_roles(self, id_project: int) -> list[ProjectRolesResponse]:
        stmt = text("""
            select * from projects_roles where id_project = :id_project
        """)

        params = {"id_project": id_project}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchall()
            return [ProjectRolesResponse(
                id=i.id,
                id_project=i.id_project,
                name=i.name
            )
                for i in data
            ]

    async def create_role(self, role: ProjectRolesRequest) -> int:
        stmt = text("""
            insert into projects_roles (id_project, name)
            values(:id_project, :name)
            returning id
        """)

        params = role.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            return data.id

    async def delete_roles_by_id(self, id_: int) -> bool:
        person_project_role_storage = PersonProjectRoleStorage(Session)
        stmt = text("""
            delete from projects_roles where id = :id
        """)
        params = {"id": id_}
        async with self.get_session() as session:
            session: AsyncSession
            await person_project_role_storage.delete_person_project_role_by_role(id_)
            await session.execute(stmt, params)
            await session.commit()
            return True

    async def delete_roles_by_id_project(self, id_project: int) -> bool:
        person_project_role_storage = PersonProjectRoleStorage(Session)
        stmt = text("""
            delete from projects_roles where id_project = :id_project
        """)
        params = {"id_project": id_project}
        async with self.get_session() as session:
            session: AsyncSession
            roles = await self.get_roles(id_project)
            for i in roles:
                await person_project_role_storage.delete_person_project_role_by_role(i.id)
            await session.execute(stmt, params)
            await session.commit()
            return True
