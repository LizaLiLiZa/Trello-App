import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..base import BaseStorage
from ...models.person.request import CreatePersonRequest
from ...models.person.response import PersonResponse
from ...models.person.response import PersonInfoResponse
from ...models.person.request import GetOnePersonRequest
from ...models.person.request import IdRequest
from ...models.person.request import PersonInfoRequest
from ...models.person.request import PersonPasswordRequest
from ...models.person.request import JWTSchema

from ...services.auth.utils import hash_password
from ...services.auth.utils import validate_password
from ...services.auth.utils import encode_jwt
class PersonStorage(BaseStorage):
    """
        Person and db
    """
    async def create_person(self, person: CreatePersonRequest) -> int:
        stmt_persons = text("""
            insert into persons (first_name, last_name, middle_name, birthday_at, phone, email) 
            values (:first_name, :last_name, :middle_name, :birthday_at, :phone, :email)
            returning id
        """)
        
        stmt_passwords = text("""
            insert into passwords (id_person, password)
            values (:id, :password)
        """)
        
        stmt_select_by_email = text("""
            select id, first_name, last_name, middle_name, birthday_at,
                phone, email, date_modification, is_delete
            from persons where email = :email
        """)
        
        stmt_select_by_phone = text("""
            select id, first_name, last_name, middle_name, birthday_at,
                phone, email, date_modification,is_delete as is_delete
            from persons where phone = :phone
        """)
        
        async with self.get_session() as session:
            session: AsyncSession
            person_data_query = person.model_dump(mode="python")
            person_data_query["password"] = hash_password(person.password)  # Сохраняем строку хэша
            result_email = (await session.execute(
                stmt_select_by_email,
                person_data_query
            )).fetchall()
            
            if len(result_email) > 0:
                raise HTTPException(
                    status_code=422,
                    detail="Упс, пользователь с таким email уже существует"
                )

            result_phone = (await session.execute(
                stmt_select_by_phone,
                person_data_query
            )).fetchone()

            if result_phone is not None:
                raise HTTPException(
                    status_code=422,
                    detail="Пользователь с таким номером телефона уже существует"
                )

            data = (await session.execute(stmt_persons, person_data_query)).fetchone()
            await session.commit()

            person_data_query["id"] = data.id

            # Сохраняем пароль
            await session.execute(stmt_passwords, person_data_query)
            await session.commit()

            return data.id

    async def get_one_person(self, id_: int) -> PersonInfoResponse:
        stmt = text("""
            select id, first_name, last_name, middle_name, birthday_at, is_delete
            from persons
            where id = :id
        """)

        async with self.get_session() as session:
            session: AsyncSession
            person_data_query = {"id": id_}
        
            result_person = (await session.execute(stmt, person_data_query)).fetchone()
            if result_person is None:
                raise HTTPException(
                    status_code=422,
                    detail="Пользователь с таким id не найден"
                )
            return PersonInfoResponse(
                id = result_person.id,
                first_name = result_person.first_name,
                last_name = result_person.last_name,
                middle_name = result_person.middle_name,
                birthday_at = result_person.birthday_at,
                is_delete = result_person.is_delete
            )

    async def login(self, person: GetOnePersonRequest) -> PersonResponse:
        stmt = text("""
            select id, first_name, last_name, middle_name, birthday_at,
                phone, email, date_modification, is_delete
            from persons
            where phone = :phone or email = :email
        """)

        stmt_password = text("""
            select * from passwords
            where id_person = :id
            limit 1
        """)

        stmt_person_admin = text("""
            select * from persons_admin
            where id_person = :id
            limit 1
        """
        )

        async with self.get_session() as session:
            session: AsyncSession
            person_data_query = person.model_dump(mode="python")
            if "@" not in person_data_query["login"]:
                person_data_query["phone"] = int(person_data_query["login"])
                person_data_query["email"] = "example@mail.ru"
            else:
                person_data_query["email"] = person_data_query["login"]
                person_data_query["phone"] = 0
            
            result_person = (await session.execute(stmt, person_data_query)).fetchone()
            if result_person is None:
                raise HTTPException(
                    status_code=422,
                    detail="Пользователь с таким логином не найден"
                )
            
            person_data_query["id"] = result_person.id

            result_password = (await session.execute(stmt_password, person_data_query)).fetchone()
            
            # Проверяем пароль
            if result_password is None or not validate_password(person.password, result_password.password):
                raise HTTPException(status_code=422, detail="Неверно введен пароль")
            person = PersonResponse(
                id = result_person.id,
                first_name = result_person.first_name,
                last_name = result_person.last_name,
                middle_name = result_person.middle_name,
                birthday_at = result_person.birthday_at,
                phone = result_person.phone,
                email = result_person.email,
                is_delete = result_person.is_delete,
                date_modification = result_person.date_modification,
                date_modification_password = result_password.date_modification
            )
            jwt_payload = {
                "sub": str(person.id)
            }
            person_admin = (await session.execute(stmt_person_admin, person_data_query)).fetchone()
            if person_admin is None:
                jwt_payload["role"] =  "user"
            else:
                jwt_payload["role"] =  "admin"
            token = encode_jwt(jwt_payload)
            return person, JWTSchema(
                access_token=token,
                token_type="Bearer"
            )

    async def get_all_persons(self) -> PersonResponse:

        stmt_persons = text("""
            select id, first_name, last_name, middle_name, birthday_at,
                phone, email, date_modification, is_delete
            from persons
        """)

        async with self.get_session() as session:
            session: AsyncSession
            result = (await session.execute(stmt_persons)).fetchall()
            print(result)
            return [
                PersonResponse(
                    id = i.id,
                    first_name = i.first_name,
                    last_name = i.last_name,
                    middle_name = i.middle_name,
                    birthday_at = i.birthday_at,
                    phone = i.phone,
                    email = i.email,
                    date_modification = i.date_modification,
                    is_delete = i.is_delete
                ) for i in result
            ]

    async def update_person_del(self, person: GetOnePersonRequest) -> str:
        result_person = await self.get_one_person(person)

        stmt = text("""
            update persons set is_delete = :is_delete
            where id = :id 
        """)

        params = {
            "id": result_person.id,
            "is_delete": True
        }

        if result_person.is_delete == True:
            params["is_delete"] = False
        async with self.get_session() as session:
            session: AsyncSession
            await session.execute(stmt, params)
            await session.commit()
            if not params["is_delete"]:
                return "Ваш аккаунт успешно восстановлен"
            return "У вас есть возможность восстановить аккаунт в течении 3 месяцев!"

    async def delete_person_admin(self, person: IdRequest) -> str:
        
        stmt_persons_delete = text("""
            delete from persons where id = :id
        """)

        stmt_passwords_delete = text("""
            delete from passwords where id_person = :id
        """)

        stmt_by_id = text("""
            select * from persons
            join passwords on persons.id = :id and passwords.id_person = :id
        """)

        async with self.get_session() as session:
            session: AsyncSession
            params = person.model_dump(mode="pthon")
            result = (await session.execute(stmt_by_id, params)).fetchall()
            if len(result) == 0:
                raise HTTPException(status_code=422, detail="Пользователь с таким id не найден.")
            await session.execute(stmt_persons_delete, params)
            await session.execute(stmt_passwords_delete, params)
            await session.commit()
            result = (await session.execute(stmt_by_id, params)).fetchall()
            if len(result) == 0:
                return "Пользователь успешно удален."

    async def update_person(self, person: PersonInfoRequest) -> PersonResponse:
       

        stmt_update = text("""
            update persons set first_name = :first_name, last_name = :last_name, middle_name = :middle_name,
                    birthday_at = :birthday_at,  date_modification = :date_modification
            where id =:id
        """)

        stmt_select = text("""
            select persons.id, persons.first_name, persons.last_name, persons.middle_name, persons.birthday_at,
                persons.phone, persons.email, persons.date_modification as persons_date_modification,
                persons.is_delete, passwords.date_modification as passwords_date_modification
            from persons join passwords on persons.id = passwords.id_person where persons.id = :id
            limit 1
        """)

        async with self.get_session() as session:
            session: AsyncSession
            params = person.model_dump(mode="python")
            params["date_modification"] = datetime.datetime.now()

            result = (await session.execute(stmt_select, params)).fetchone()
            if result is None:
                raise HTTPException(status_code=422, detail="Нет пользователя с таким id.")

            await session.execute(stmt_update, params)
            await session.commit()

            result = (await session.execute(stmt_select, params)).fetchone()

            return PersonResponse(
                id = result.id,
                first_name = result.first_name,
                last_name = result.last_name,
                middle_name = result.middle_name,
                birthday_at = result.birthday_at,
                phone = result.phone,
                email = result.email,
                is_delete = result.is_delete,
                date_modification = result.persons_date_modification,
                date_modification_password = result.passwords_date_modification
            )

    async def update_password_person(self, password: PersonPasswordRequest) -> PersonResponse:
        
        stmt_find = text("""
            select * from passwords
            where id_person = :id
        """)

        stmt_update = text("""
            update passwords set password = :new_password, date_modification = :date_modification
            where id_person = :id
        """)

        stmt_select_person = text("""
            select persons.id, persons.first_name, persons.last_name, persons.middle_name, persons.birthday_at,
                persons.phone, persons.email, persons.date_modification as persons_date_modification,
                persons.is_delete, passwords.date_modification as passwords_date_modification
            from persons join passwords on persons.id = passwords.id_person where persons.id = :id
            limit 1
        """)

        params = password.model_dump(mode="python")
        params["date_modification"] = datetime.datetime.now()
        print(params)
        async with self.get_session() as session:
            session: AsyncSession
            print(1)
            result_password = (await session.execute(stmt_find, params)).fetchone()
            if result_password is None or not validate_password(password.password, result_password.password):
                raise HTTPException(status_code=422, detail="Неверно введен пароль.")
            new_password = hash_password(password.new_password)
            params["new_password"] = new_password
            print(params)
            await session.execute(stmt_update, params)
            await session.commit()

            result = (await session.execute(stmt_select_person, params)).fetchone()
            return PersonResponse(
                id = result.id,
                first_name = result.first_name,
                last_name = result.last_name,
                middle_name = result.middle_name,
                birthday_at = result.birthday_at,
                phone = result.phone,
                email = result.email,
                is_delete = result.is_delete,
                date_modification = result.persons_date_modification,
                date_modification_password = result.passwords_date_modification
            )
