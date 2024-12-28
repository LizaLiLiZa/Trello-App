from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseStorage

class DeleteStorage(BaseStorage):
    async def delete_task(self, id_task) -> bool:
        params = {"id_task": id_task}
        delete_task_mean_date = text("""
            delete from tasks_date
            where id in (
                select tasks_date.id
                from tasks_means
                join tasks_date on tasks_means.id_mean = tasks_date.id
                join tasks_categories on tasks_categories.id = tasks_means.id_task_categories
                where tasks_means.id_task = :id_task
            )
        """)
        delete_task_mean_person = text("""
            delete from tasks_person
            where id in (
                select tasks_person.id
                from tasks_means
                join tasks_person on tasks_means.id_mean = tasks_person.id
                join tasks_categories on tasks_categories.id = tasks_means.id_task_categories
                where tasks_means.id_task = :id_task
            )
        """)
        delete_task_mean = text("""
            delete from tasks_means where id_task = :id_task
        """)
        delete_task = text("""
            delete from tasks where id = :id_task
        """)
        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(delete_task_mean_date, params)
            await session.commit()
            await session.execute(delete_task_mean_person, params)
            await session.commit()
            await session.execute(delete_task_mean, params)
            await session.commit()
            await session.execute(delete_task, params)
            await session.commit()
            return True

    async def delete_state(self, id_state) -> bool:
        params = {"id_state": id_state}
        delete_state = text("""
            delete from states where id = :id_state
        """)
        select_task = text("""
            select * from tasks where id_state = :id_state
        """)
        async with self.get_session() as session:
            session: AsyncSession
            tasks = (await session.execute(select_task, params)).fetchall()
            for i in tasks:
                await self.delete_task(i.id)
            await session.execute(delete_state, params)
            await session.commit()
            return True

    async def delete_board(self, id_board) -> bool:
        params = {"id_board": id_board}
        delete_state = text("""
            delete from boards where id = :id_board
        """)
        select_task = text("""
            select * from states where id_board = :id_board
        """)
        async with self.get_session() as session:
            session: AsyncSession
            states = (await session.execute(select_task, params)).fetchall()
            for i in states:
                await self.delete_state(i.id)
            await session.execute(delete_state, params)
            await session.commit()
            return True

    async def delete_project(self, id_project) -> bool:
        params = {"id_project": id_project}
        delete_project = text("""
            delete from projectS where id = :id_project
        """)
        select_boards = text("""
            select * from boards where id_project = :id_project
        """)
        async with self.get_session() as session:
            session: AsyncSession
            boards = (await session.execute(select_boards, params)).fetchall()
            for i in boards:
                await self.delete_board(i.id)
            await session.execute(delete_project, params)
            await session.commit()
            return True

    async def delete_person(self, id_person) -> bool:
        params = {"id_person": id_person}
        select_boards = text("""
            select * from projects where id_person = :id_person
        """)
        async with self.get_session() as session:
            session: AsyncSession
            projects = (await session.execute(select_boards, params)).fetchall()
            for i in projects:
                await self.delete_project(i.id)
            return True

