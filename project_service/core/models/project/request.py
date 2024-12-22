# pylint: disable=E0213
import datetime
from typing import Optional
from pydantic import BaseModel

class CreateProjectRequest(BaseModel):
    """
        Request create project
    """
    id_person: int
    name: str
    description: Optional[str] = None
    date_created: datetime.datetime

class UpdateProjectRequest(BaseModel):
    """
        Request update project
    """

    id: int
    name: str
    description: Optional[str] = None
