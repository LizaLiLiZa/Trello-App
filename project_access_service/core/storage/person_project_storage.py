from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import Session
from .person_project_role_storage import PersonProjectRoleStorage
from .role_storage import RoleStorage

from .base import BaseStorage

from ..models.person_project.request import PersonProjectRequest
from ..models.person_project.request import UpdateAccessRightRequest

from ..models.person_project.response import PersonProjectResponse

from ..services.auth.utils import encode_jwt

person_project_role_storage = PersonProjectRoleStorage(Session)
role_storage = RoleStorage(Session)

class PersonProjectStorage(BaseStorage):
    async def get_persons_project_by_id(self, id_person_project: int) -> PersonProjectResponse:
        stmt = text("""
            select * from persons_projects where id = :id_person_project
        """)

        params = {"id_person_project": id_person_project}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchall()
            return PersonProjectResponse(
                id=data.id,
                id_person=data.id_person,
                id_project=data.id_project,
                id_access_rights=data.id_access_rights
            )

    async def get_persons_project(self, id_project: int) -> list[PersonProjectResponse]:
        stmt = text("""
            select * from persons_projects where id_project = :id_project
        """)

        params = {"id_project": id_project}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchall()
            return [PersonProjectResponse(
                id=i.id,
                id_person=i.id_person,
                id_project=i.id_project,
                id_access_rights=i.id_access_rights
            )
                for i in data
            ]

    async def get_person_project(self, id_project: int, id_person: int) -> PersonProjectResponse:
        stmt = text("""
            select * from persons_projects 
            where id_project = :id_project and id_person = :id_person
        """)
        stmt_access_rights = text("""
            select * from access_rights where id = :id_access_rights
        """)

        params = {"id_project": id_project,
                  "id_person" : id_person}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            params["id_access_rights"] = data.id_access_rights
            access_right = (await session.execute(stmt_access_rights, params)).fetchone()
            jwt_payload = {
                "sub": str(id_person),
                "role": access_right.name,                
                "id_project": id_project
            }
            token = encode_jwt(jwt_payload)
            return PersonProjectResponse(
                id=data.id,
                id_person=data.id_person,
                id_project=data.id_project,
                id_access_rights=data.id_access_rights
            ), token
    
    async def create_project(self, person_project: PersonProjectRequest) -> int:
        stmt = text("""
            insert into persons_projects (id_person, id_project, id_access_rights)
            values(:id_person, :id_project, :id_access_rights)
            returning id
        """)

        stmt_access_rights = text("""
            select * from access_rights where id = :id_access_rights
        """)

        params = person_project.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            access_right = (await session.execute(stmt_access_rights, params)).fetchone()
            jwt_payload = {
                "sub": str(person_project.id_person),
                "role": access_right.name,
                "id_project": person_project.id_project
            }
            token = encode_jwt(jwt_payload)
            return data.id, token

    async def create_person_project(self, person_project: PersonProjectRequest) -> int:
        stmt = text("""
            insert into persons_projects (id_person, id_project, id_access_rights)
            values(:id_person, :id_project, :id_access_rights)
            returning id
        """)


        params = person_project.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            return data.id

    async def update_person_project(self, person_project: UpdateAccessRightRequest) -> PersonProjectResponse:
        stmt = text("""
            update persons_projects set  id_access_rights = :id_access_rights
            where id = :id
        """)

        params = person_project.model_dump(mode="python")

        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            return await self.get_person_project(person_project.id_project, person_project.id_person)

    async def delete_person_project_by_person(self, id_person: int, id_project: int) -> bool:
        stmt = text("""
            delete from persons_projects where id_project = :id_project and id_person = :id_person
            returning id
        """)

        params = {"id_person": id_person,
                  "id_project": id_project}

        async with self.get_session() as session:
            session: AsyncSession
            data = (await session.execute(stmt, params)).fetchone()
            await session.commit()
            await person_project_role_storage.delete_person_project_role_by_person_project(data.id)
            return True

    async def delete_person_project_by_project(self, id_project) -> bool:
        all_persons = await self.get_persons_project(id_project)
        for i in all_persons:
            await self.delete_person_project_by_person(i.id_person, i.id_project)
        await role_storage.delete_roles_by_id_project(id_project)
        return True