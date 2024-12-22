# pylint: disable=E0213
import datetime
from typing import Optional
from pydantic import BaseModel

class TaskRequest(BaseModel):
    id_state: int
    id_low_task: Optional[int] = None
    name: str
    description: str
    date_created: datetime.datetime

class TaskCategoriesRequest(BaseModel):
    id_project: int
    name: str
    type: str

class TaskTextRequest(BaseModel):
    text: str
    id_task_categories: int

class TaskDateRequest(BaseModel):
    date: datetime.datetime
    id_task_categories: int

class TaskPersonRequest(BaseModel):
    id_person: int
    id_task_categories: int

class TaskMeanRequest(BaseModel):
    id_task_categories: int
    id_mean: int
    id_task: int
