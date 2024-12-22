# pylint: disable=E0213
import datetime
from typing import Optional
from pydantic import BaseModel

class TaskResponse(BaseModel):
    id: int
    id_state: int
    id_low_task: Optional[int] = None
    name: str
    description: str
    date_created: datetime.datetime

class TaskTextResponse(BaseModel):
    id: int
    id_task_categories: int
    text: str

class TaskTextCategoriesResponse(BaseModel):
    id: int
    id_text: int
    id_task_categories: int
    text_: str
    name: str

class TaskMeanTextResponse(BaseModel):
    id_task: int
    data: list[TaskTextCategoriesResponse]

class TaskDateResponse(BaseModel):
    id: int
    id_task_categories: int
    date: datetime.datetime

class TaskPersonResponse(BaseModel):
    id: int
    id_task_categories: int
    id_person: int

class TaskCategoriesResponse(BaseModel):
    id: int
    id_project: int
    name: str
    type: str
