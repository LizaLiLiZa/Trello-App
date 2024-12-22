# pylint: disable=E0213
import datetime
from typing import Optional
from pydantic import BaseModel

class ProjectResponse(BaseModel):
    id: int
    id_person: int
    name: str
    description: Optional[str] = None
    date_created: datetime.datetime
