# pylint: disable=E0213
from pydantic import BaseModel

class PersonProjectRolesRequest(BaseModel):
    id_person_project: int
    id_role: int