# pylint: disable=E0213
import datetime
from typing import Optional
from pydantic import BaseModel

class AccessRightsRequest(BaseModel):
    date_created: datetime.datetime
    name: str
