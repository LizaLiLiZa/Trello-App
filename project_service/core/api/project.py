from fastapi import APIRouter
from ..storage import project_storage

from ..models.project.request import CreateProjectRequest
from ..models.project.response import ProjectResponse
from ..models.project.request import UpdateProjectRequest

router = APIRouter(tags=["Project"])

@router.post("/project")
async def create_project(project: CreateProjectRequest) -> list[ProjectResponse]:
    return await project_storage.create_project(project)

@router.get("/project")
async def get_projects(id_person: int) -> list[ProjectResponse]:
    return await project_storage.get_project(id_person)

@router.patch("/project")
async def update_projects(project: UpdateProjectRequest) -> ProjectResponse:
    return await project_storage.update_project(project)

@router.delete("/project")
async def delete_project(id_project: int) -> bool:
    return await project_storage.delete_project(id_project)
