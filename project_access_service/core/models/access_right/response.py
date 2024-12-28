# pylint: disable=E0213
import datetime
from pydantic import BaseModel

class AccessRightsResponse(BaseModel):
    id: int
    date_created: datetime.datetime
    name: str
