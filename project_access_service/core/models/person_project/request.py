# pylint: disable=E0213
from pydantic import BaseModel

class PersonProjectRequest(BaseModel):
    id_person: int
    id_person_creater: int
    id_project: int
    id_access_rights: int

class UpdateAccessRightRequest(BaseModel):
    id: int
    id_project: int
    id_person: int
    id_access_rights: int
