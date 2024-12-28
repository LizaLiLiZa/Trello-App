# pylint: disable=E0213
from pydantic import BaseModel

class ProjectRolesResponse(BaseModel):
    id: int
    id_project: int
    name: str
