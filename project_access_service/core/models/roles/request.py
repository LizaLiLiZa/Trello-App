# pylint: disable=E0213
from pydantic import BaseModel

class ProjectRolesRequest(BaseModel):
    id_project: int
    name: str
