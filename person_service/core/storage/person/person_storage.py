import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..base import BaseStorage
from ...models.person.request import CreatePersonRequest
from ...models.person.response import PersonResponse
from ...models.person.request import GetOnePersonRequest
from ...models.person.request import IdRequest
from ...models.person.request import PersonInfoRequest
from ...models.person.request import PersonPasswordRequest

class PersonStorage(BaseStorage):
    """
        Person and db
    """
    async def create_person(self, person: CreatePersonRequest) -> PersonResponse:
        """
            Creates a new person in the database along with their associated password.

            This function performs the following steps:
            1. Validates that the provided email is not already associated with an existing person.
            2. Validates that the provided phone number is not already associated with an existing person.
            3. Inserts a new record in the `persons` table with the provided details.
            4. Fetches the ID of the newly created person to associate a password with them.
            5. Inserts the password into the `passwords` table linked to the new person.
            6. Returns the details of the newly created person as a `PersonResponse` object.

            Args:
                person (PersonCreateRequest): An object containing the following fields:
                    - `first_name` (str): The first name of the person.
                    - `last_name` (str): The last name of the person.
                    - `middle_name` (str): The middle name of the person, if applicable.
                    - `birthday_at` (date): The date of birth of the person.
                    - `phone` (str): The phone number of the person.
                    - `email` (str): The email address of the person.
                    - `password` (str): The password to associate with the new person's account.

            Returns:
                PersonResponse: An object containing the person's details:
                    - `id` (int): The unique identifier of the person.
                    - `first_name` (str): The first name of the person.
                    - `last_name` (str): The last name of the person.
                    - `middle_name` (str): The middle name of the person.
                    - `birthday_at` (date): The date of birth of the person.
                    - `phone` (str): The phone number of the person.
                    - `email` (str): The email address of the person.
                    - `is_delete` (bool): The deletion status of the person (`False` by default for new persons).
                    - `date_modification` (datetime): The timestamp of the person's record creation or last update.
                    - `date_modification_password` (datetime): The timestamp of the password's creation.

            Raises:
                HTTPException: If:
                    - The email is already in use (status_code=422, detail="Упс, пользователь с таким email уже существует").
                    - The phone number is already in use (status_code=422, detail="Пользователь с таким номером телефона уже существует").
        """

        stmt_persons = text("""
            insert into persons (first_name, last_name, middle_name, birthday_at, phone, email) 
            values (:first_name, :last_name, :middle_name, :birthday_at, :phone, :email
            )
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

            if result_phone != None:
                raise HTTPException(
                    status_code=422,
                    detail="Пользователь с таким номером телефона уже существует"
                    )

            await session.execute(stmt_persons, person_data_query)
            await session.commit()

            result = (await session.execute(stmt_select_by_phone, person_data_query)).fetchone()
            person_data_query["id"] = int(result.id)

            await session.execute(stmt_passwords, person_data_query)
            await session.commit()

            return PersonResponse(
                id=result.id,
                first_name=result.first_name,
                last_name=result.last_name,
                middle_name=result.middle_name,
                birthday_at=result.birthday_at,
                phone=result.phone,
                email=result.email,
                is_delete = result.is_delete,
                date_modification = result.date_modification,
                date_modification_password = result.date_modification
            )

    async def get_one_person(self, person: GetOnePersonRequest) -> PersonResponse:
        """
            Retrieves a person's details using their login and password.

            This function performs the following operations:
            1. Determines if the login provided is an email or phone number.
            2. Queries the database for a person matching the provided login (email or phone).
            3. Verifies if the provided password matches the stored password for the found person.
            4. Returns the person's details as a `PersonResponse` object if the login and password are correct.

            Args:
                person (PersonLoginRequest): An object containing the following fields:
                    - `login` (str): The login credential, which can be an email or a phone number.
                    - `password` (str): The password associated with the person's account.

            Returns:
                PersonResponse: An object containing the person's details:
                    - `id` (int): The unique identifier of the person.
                    - `first_name` (str): The first name of the person.
                    - `last_name` (str): The last name of the person.
                    - `middle_name` (str): The middle name of the person, if available.
                    - `birthday_at` (date): The date of birth of the person.
                    - `phone` (str): The phone number of the person.
                    - `email` (str): The email address of the person.
                    - `is_delete` (bool): The deletion status of the person (`True` for deleted, `False` for active).
                    - `date_modification` (datetime): The last modification date of the person's record.
                    - `date_modification_password` (datetime): The last modification date of the password.

            Raises:
                HTTPException: If:
                    - No person is found with the provided login (status_code=422, detail="Пользователь с таким логином не найден").
                    - The password is incorrect (status_code=422, detail="Неверно введен пароль").
        """

        stmt = text("""
            select id, first_name, last_name, middle_name, birthday_at,
                phone, email, date_modification, is_delete
            from persons
            where phone = :phone or email = :email
        """)

        stmt_password = text("""
            select * from passwords
            where password = :password and id_person = :id
            limit 1
        """)

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
            if result_password is None:
                raise HTTPException(status_code=422, detail="Неверно введен пароль")
            return PersonResponse(
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

    async def get_all_persons(self) -> PersonResponse:
        """
            Retrieves all persons from the database.

            This function performs the following operations:
            1. Executes a query to select all records from the `persons` table.
            2. Maps the resulting database rows to a list of `PersonResponse` objects.

            Each `PersonResponse` includes the following fields:
            - `id` (int): The unique identifier of the person.
            - `first_name` (str): The first name of the person.
            - `last_name` (str): The last name of the person.
            - `middle_name` (str): The middle name of the person, if available.
            - `birthday_at` (date): The date of birth of the person.
            - `phone` (str): The phone number of the person.
            - `email` (str): The email address of the person.
            - `date_modification` (datetime): The last modification date of the person's record.
            - `is_delete` (bool): The deletion status of the person (`True` for deleted, `False` for active).

            Args:
                None

            Returns:
                List[PersonResponse]: A list of all persons represented as `PersonResponse` objects.

            Raises:
                No specific exceptions are raised in this function, but any issues during database interaction 
                (e.g., connection errors) will propagate as standard exceptions.
        """

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
        """
            Toggles the deletion status (`is_delete` field) of a user in the database.

            This function performs the following operations:
            1. Retrieves the user's current information by their unique ID.
            2. Updates the `is_delete` field in the `persons` table to its opposite value (`True` or `False`).
            - If `is_delete` is currently `True` (indicating the account is deleted), it is set to `False` (restoring the account).
            - If `is_delete` is `False`, it is set to `True` (marking the account as deleted).
            3. Commits the change to the database and returns an appropriate message based on the new `is_delete` status.

            Args:
                person (PersonRequest): An object containing:
                    - `id` (int): The unique identifier of the user whose `is_delete` field is to be toggled.

            Returns:
                str: A message indicating the outcome:
                    - "Ваш аккаунт успешно восстановлен" (if the account was restored).
                    - "У вас есть возможность восстановить аккаунт в течении 3 месяцев!" (if the account was marked as deleted).

            Raises:
                HTTPException: If the user with the specified `id` does not exist, an error is raised during the call to 
                `get_one_person`.
        """
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
        """
            Deletes a user and their associated password record from the database using their unique ID.

            This function performs the following operations:
            1. Verifies that a user with the specified `id` exists in the database by checking both the `persons` and 
            `passwords` tables.
            2. Deletes the user record from the `persons` table and their associated password record from the `passwords` table.
            3. Confirms the deletion by ensuring no records with the specified `id` remain in the database.

            Args:
                person (PersonDeleteRequest): An object containing:
                    - `id` (int): The unique identifier of the user to be deleted.

            Returns:
                str: A success message confirming the user has been deleted, specifically:
                    - "Пользователь успешно удален."

            Raises:
                HTTPException: If no user is found with the specified `id`:
                    - Status Code 422: "Пользователь с таким id не найден."
        """

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
        """
            Updates the personal details of a user, including first name, last name, middle name, and date of birth.

            This function performs the following operations:
            1. Checks if a user with the specified `id` exists in the database.
            2. Updates the user's personal details (`first_name`, `last_name`, `middle_name`, and `birthday_at`) and 
            sets a new `date_modification` timestamp.
            3. Fetches and returns the updated user details, including password modification information.

            Args:
                person (PersonUpdateRequest): An object containing:
                    - `id` (int): The unique identifier of the user.
                    - `first_name` (str): The updated first name of the user.
                    - `last_name` (str): The updated last name of the user.
                    - `middle_name` (str): The updated middle name of the user.
                    - `birthday_at` (datetime): The updated date of birth for the user.

            Returns:
                PersonResponse: An object containing:
                    - `id` (int): The user's unique identifier.
                    - `first_name` (str): The user's updated first name.
                    - `last_name` (str): The user's updated last name.
                    - `middle_name` (str): The user's updated middle name.
                    - `birthday_at` (datetime): The user's updated date of birth.
                    - `phone` (str): The user's phone number.
                    - `email` (str): The user's email address.
                    - `is_delete` (bool): Logical deletion flag for the user.
                    - `date_modification` (datetime): The timestamp of the user's profile modification.
                    - `date_modification_password` (datetime): The timestamp of the last password modification.

            Raises:
                HTTPException: If no user is found with the specified `id`:
                    - Status Code 422: "Нет пользователя с таким id."
        """

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
        """
            Updates the password for a specified user.

            This function performs the following operations:
            1. Validates the existence of a user with the given `id` and `password`.
            2. Updates the user's password and records the modification timestamp.
            3. Fetches and returns the updated user details.

            Args:
                password (PersonPasswordRequest): An object containing:
                    - `id` (int): The user's unique identifier.
                    - `password` (str): The current password for verification.
                    - `new_password` (str): The new password to be set.

            Returns:
                PersonResponse: An object containing:
                    - `id` (int): The user's unique identifier.
                    - `first_name` (str): The user's first name.
                    - `last_name` (str): The user's last name.
                    - `middle_name` (str): The user's middle name.
                    - `birthday_at` (datetime): The user's date of birth.
                    - `phone` (str): The user's phone number.
                    - `email` (str): The user's email address.
                    - `is_delete` (bool): Logical deletion flag for the user.
                    - `date_modification` (datetime): The timestamp of the user's profile modification.
                    - `date_modification_password` (datetime): The timestamp of the last password modification.

            Raises:
                HTTPException: If no user is found with the specified `id` and `password`:
                    - Status Code 422: "Неверно введен пароль."
        """
        stmt_find = text("""
            select * from passwords
            where id_person = :id and password = :password
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
            result = (await session.execute(stmt_find, params)).fetchone()
            if result is None:
                raise HTTPException(status_code=422, detail="Неверно введен пароль.")

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
