from fastapi import APIRouter

from ..storage import task_storage
from ..models.tasks.responses import TaskResponse
from ..models.tasks.requests import TaskRequest

router = APIRouter(tags=["Task"])

@router.get("/task")
async def get_task(id_state: int) -> list[TaskResponse]:
    return await task_storage.get_task(id_state)

@router.post("/task")
async def create_task(task: TaskRequest) -> int:
    return await task_storage.create_task(task)

@router.patch("/task")
async def upadate_task(task: TaskResponse) -> TaskResponse:
    return await task_storage.update_task(task)
