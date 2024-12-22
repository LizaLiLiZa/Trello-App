# pylint: disable=E0213
import datetime
from pydantic import BaseModel

class StateRequest(BaseModel):
    id_board: int
    name: str
    date_created: datetime.datetime
