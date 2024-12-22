# pylint: disable=E0213
from typing import Optional
from datetime import datetime
from .requests import BoardRequest

class BoardResponse(BoardRequest):
    id: int
    id_project: int
    name: str
    description: Optional[str] = None
    date_created: datetime
