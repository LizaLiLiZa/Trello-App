# pylint: disable=E0213
import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, EmailStr, TypeAdapter, ValidationError
from fastapi import HTTPException

from ...services.validate.validate import ValidateInfo

class CreatePersonRequest(BaseModel):
    """
        Request create person
    """
    first_name: str
    last_name: str
    middle_name:  Optional[str] = None
    birthday_at: datetime.date
    phone: int
    email: EmailStr
    password: str

    @field_validator("first_name")
    def validate_first_name(cls, value: str):
        """
            Validation first name
        """        
        value = value.capitalize()
        if ValidateInfo.validation_name(value):
            return value
        raise HTTPException(status_code=422, detail="Неверно введено имя пользователя!")

    @field_validator("last_name")
    def validate_last_name(cls, value: str):
        """
            Validation last name
        """
        value = value.capitalize()
        if ValidateInfo.validation_name(value):
            return value
        raise HTTPException(status_code=422, detail="Неверно введена фамилия пользователя!")

    @field_validator("middle_name")
    def validate_middle_name(cls, value: str):
        """
            Validation middle name
        """
        value = value.capitalize()
        if value is None or ValidateInfo.validation_name(value):
            return value
        raise HTTPException(status_code=422, detail="Неверно введено отчество пользователя!")

    @field_validator("birthday_at")
    def validate_birthday_at(cls, value: datetime.date):
        """
            Validation birthday
        """
        if ValidateInfo.validation_birthday_at(value):
            return value
        raise HTTPException(status_code=422, detail="Вам должно быть больше 12 лет и меньше 120!")

    @field_validator("phone")
    def validate_phone(cls, value: int):
        """
            Validation phone
        """
        if ValidateInfo.validate_phone(str(value)):
            return value
        raise HTTPException(status_code=422, detail="Неверный формат телефона")

    @field_validator("password")
    def validate_password(cls, value: str):
        """
            Validate password
        """
        if ValidateInfo.validate_password(value):
            return value
        raise HTTPException(status_code=422, detail="Неверный формат пароля")

class GetOnePersonRequest(BaseModel):
    """
    Request to get person by login and password
    """
    password: str
    login: str

    @field_validator("password")
    def validate_password(cls, value: str):
        """
        Validate password format
        """
        if not value:
            raise HTTPException(status_code=422, detail="Пароль не может быть пустым")
        if ValidateInfo.validate_password(value):
            return value
        raise HTTPException(status_code=422, detail="Неверно введен пароль")

    @field_validator("login")
    def validate_login(cls, value: str):
        """
        Validate login format (email or phone)
        """
        if not value:
            raise HTTPException(status_code=422, detail="Логин не может быть пустым")

        if "@" in value:
            try:
                TypeAdapter(EmailStr).validate_python(value)
                return value
            except ValidationError as exc:
                raise HTTPException(status_code=422, detail="Неверный формат e-mail.") from exc 
        else:
            if ValidateInfo.validate_phone(value):
                return value
            raise HTTPException(status_code=422, detail="Неверный формат телефона.")

class IdRequest(BaseModel):
    """
        Request id persons
    """
    id: int

class PersonInfoRequest(BaseModel):
    """
        Get person info
    """
    id: int
    first_name: str
    last_name: str
    middle_name: str
    birthday_at: datetime.date

    @field_validator("first_name")
    def validate_first_name(cls, value: str):
        """
            Validation first name
        """        
        value = value.capitalize()
        if ValidateInfo.validation_name(value):
            return value
        raise HTTPException(status_code=422, detail="Неверно введено имя пользователя!")

    @field_validator("last_name")
    def validate_last_name(cls, value: str):
        """
            Validation last name
        """
        value = value.capitalize()
        if ValidateInfo.validation_name(value):
            return value
        raise HTTPException(status_code=422, detail="Неверно введена фамилия пользователя!")

    @field_validator("middle_name")
    def validate_middle_name(cls, value: str):
        """
            Validation middle name
        """
        value = value.capitalize()
        if value is None or ValidateInfo.validation_name(value):
            return value
        raise HTTPException(status_code=422, detail="Неверно введено отчество пользователя!")

    @field_validator("birthday_at")
    def validate_birthday_at(cls, value: datetime.date):
        """
            Validation birthday
        """
        if ValidateInfo.validation_birthday_at(value):
            return value
        raise HTTPException(status_code=422, detail="Вам должно быть больше 12 лет и меньше 120!")

class PersonPasswordRequest(BaseModel):
    """
        Password person
    """
    id: int
    password: str
    new_password: str

    @field_validator("password")
    def password_validate(cls, value: str):
        if ValidateInfo.validate_password(value):
            return value
        raise HTTPException(status_code=422, detail="Неверный формат старого пароля.")

    @field_validator("new_password")
    def new_password_validate(cls, value: str):
        if ValidateInfo.validate_password(value):
            return value
        raise HTTPException(status_code=422, detail="Неверный формат нового пароля.")
