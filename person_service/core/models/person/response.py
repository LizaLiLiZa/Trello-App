# pylint: disable=E0213
import datetime
from typing import Optional
from pydantic import BaseModel

class PersonResponse(BaseModel):
    """
        Response person
    """
    id: int
    first_name: str
    last_name: str
    middle_name:  Optional[str] = None
    birthday_at: datetime.date
    phone: int
    email: str
    date_modification: datetime.datetime
    is_delete: bool
    date_modification_password: Optional[datetime.datetime] = None

class PersonInfoResponse(BaseModel):
    """
        Response person
    """
    id: int
    first_name: str
    last_name: str
    middle_name:  Optional[str] = None
    birthday_at: datetime.date
    is_delete: bool
