from fastapi import APIRouter

from ..storage import task_mean_storage

from ..models.tasks.requests import TaskTextRequest
from ..models.tasks.requests import TaskDateRequest
from ..models.tasks.requests import TaskPersonRequest
from ..models.tasks.requests import TaskMeanRequest
from ..models.tasks.requests import TaskMeanUpdateRequest

from ..models.tasks.responses import TaskTextResponse
from ..models.tasks.responses import TaskMeanTextResponse
from ..models.tasks.responses import TaskMeanResponse
from ..models.tasks.responses import TaskMeanDateResponse
from ..models.tasks.responses import TaskMeanPersonResponse

router = APIRouter(tags=["Task Mean"])

@router.get("/task-mean-text")
async def get_task_mean_text(id_task: int) -> TaskMeanTextResponse:
    return await task_mean_storage.get_task_mean_text(id_task)

@router.get("/task-mean-date")
async def get_task_mean_date(id_task: int) -> TaskMeanDateResponse:
    return await task_mean_storage.get_task_mean_date(id_task)

@router.get("/task-mean-person")
async def get_task_mean_person(id_task: int) -> TaskMeanPersonResponse:
    return await task_mean_storage.get_task_mean_person(id_task)

@router.post("/task-mean")
async def create_task_mean(task_mean: TaskMeanRequest) -> int:
    return await task_mean_storage.create_task_mean(task_mean)

@router.patch("/task-mean")
async def update_task_mean(task_mean: TaskMeanUpdateRequest) -> TaskMeanResponse:
    return await task_mean_storage.update_task_mean(task_mean)

@router.delete("/task-mean")
async def delete_task_mean(id_task_mean: int) -> bool:
    return await task_mean_storage.delete_task_mean(id_task_mean)

@router.get("/mean-text")
async def get_mean_text(id_categories: int) -> list[TaskTextResponse]:
    return await task_mean_storage.get_text(id_categories)

@router.post("/mean-text")
async def create_mean_text(text_: TaskTextRequest) -> int:
    return await task_mean_storage.create_text(text_)

@router.post("/mean-date")
async def create_mean_date(date: TaskDateRequest) -> int:
    return await task_mean_storage.create_date(date)

@router.post("/mean-person")
async def create_mean_post(person: TaskPersonRequest) -> int:
    return await task_mean_storage.create_person(person)

@router.delete("/mean-text")
async def delete_mean_text(id_: int) -> bool:
    return await task_mean_storage.delete_text(id_)

@router.delete("/mean-date")
async def delete_mean_date(id_: int) -> bool:
    return await task_mean_storage.delete_date(id_)

@router.delete("/mean-person")
async def delete_mean_person(id_: int) -> bool:
    return await task_mean_storage.delete_person(id_)
