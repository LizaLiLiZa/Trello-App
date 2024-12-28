# pylint: disable=E0213
from pydantic import BaseModel

class PersonProjectRolesResponse(BaseModel):
    id: int
    id_person_project: int
    id_role: int