# pylint: disable=E0213
from pydantic import BaseModel

class PersonProjectResponse(BaseModel):
    id: int
    id_person: int
    id_project: int
    id_access_rights: int
