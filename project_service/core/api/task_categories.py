from fastapi import APIRouter

from ..storage import task_categories_storage

from ..models.tasks.requests import TaskCategoriesRequest
from ..models.tasks.responses import TaskCategoriesResponse

router = APIRouter(tags=["Task Categories"])

@router.get("/task-categories")
async def get_task_categories(id_project: int) -> list[TaskCategoriesResponse]:
    return await task_categories_storage.get_categories_by_id_project(id_project)

@router.post("/task-categories")
async def create_task_categories(task_categories: TaskCategoriesRequest) -> int:
    return await task_categories_storage.create_categories(task_categories)

@router.patch("/task-categories")
async def update_task_categories(task_categories: TaskCategoriesResponse) -> TaskCategoriesResponse:
    return await task_categories_storage.update_categories(task_categories)
