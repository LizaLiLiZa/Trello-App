# pylint: disable=E0213
import datetime
from .request import StateRequest


class StateResponse(StateRequest):
    id: int
    id_board: int
    name: str
    date_created: datetime.datetime
