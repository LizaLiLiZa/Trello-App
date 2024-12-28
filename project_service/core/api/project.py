import requests
from fastapi import APIRouter,  Header, Response, HTTPException
from ..storage import project_storage

from ..models.project.request import CreateProjectRequest
from ..models.project.response import ProjectResponse
from ..models.project.request import UpdateProjectRequest

from ..service.auth.valid_token import valid_token_person
from ..service.auth.valid_token import valid_token_person_project

router = APIRouter(tags=["Project"])

@router.post("/project")
async def create_project(project: CreateProjectRequest, response: Response,
    authorization: str = Header(None)
    ) -> int:

    token = await valid_token_person(project.id_person, authorization)
    id_project = await project_storage.create_project(project)
    url = "http://127.0.0.1:8002/api/create-project"
    data = {
        "id_person": project.id_person,
        "id_person_creater": project.id_person,
        "id_project": id_project,
        "id_access_rights": 6
    }
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"  # Если требуется токен
    }
    response_new = requests.post(url, json=data, headers=headers, timeout=10)
    if response_new.status_code == 200:
        token = response_new.headers.get("Authorization")
        response.headers["Authorization"] = f"Bearer {token}"
        return id_project

@router.get("/project")
async def get_projects(id_person: int,
    authorization: str = Header(None)                   
    ) -> list[ProjectResponse]:
    token = await valid_token_person(id_person, authorization)
    if token is None:
        raise HTTPException(status_code=401, detail="Ошибка аутенефекации!")
    return await project_storage.get_project(id_person)

@router.patch("/project")
async def update_projects(project: UpdateProjectRequest,
        authorization: str = Header(None)) -> ProjectResponse:
    admin = await valid_token_person_project(project.id_person, "admin", project.id, authorization)
    if admin:
        return await project_storage.update_project(project)
    raise HTTPException(status_code=403, detail="Упс, не хватает прав доступа!")
