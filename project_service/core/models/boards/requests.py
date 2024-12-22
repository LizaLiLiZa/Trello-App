# pylint: disable=E0213
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BoardRequest(BaseModel):
    id_project: int
    name: str
    description: Optional[str] = None
    date_created: datetime