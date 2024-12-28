from fastapi import APIRouter, Response, Header, HTTPException, Depends

from ..storage import person_project_storage

from ..models.person_project.request import PersonProjectRequest
from ..models.person_project.request import UpdateAccessRightRequest

from ..models.person_project.response import PersonProjectResponse
from ..services.auth.valid_token import valid_token

from ..services.auth.auth_utils import get_current_user_role
from ..services.auth.auth_utils import get_current_user_sub
from ..services.auth.auth_utils import get_current_user_id_project
router = APIRouter(tags=["Person Project"])

@router.get("/persons-project")
async def get_persons_project(id_project: int,
        role: str = Depends(get_current_user_role),
        id_project_token: str = Depends(get_current_user_id_project)) -> list[PersonProjectResponse]:
    if str(id_project) != id_project_token:
        raise HTTPException(status_code=401, detail="Id проектов не совпадают!")
    if role == "admin" or role == "editing":
        return await person_project_storage.get_persons_project(id_project)
    raise HTTPException(status_code=401, detail="Нет прав доступа!")

@router.get("/person-project")
async def get_person_project(id_project: int, id_person: int,
    response: Response,
    authorization: str = Header(None)) -> PersonProjectResponse:
    data =  await valid_token(id_person, authorization)
    if data or not data:
        person_project, token =  await person_project_storage.get_person_project(id_project, id_person)
        response.headers["Authorization"] = f"Bearer {token}"
        return person_project
    raise HTTPException(status_code=401, detail="Нет прав доступа!")

@router.post("/create-project")
async def crate_project(person_project: PersonProjectRequest, response: Response,
        authorization: str = Header(None)) -> int:
    data = await valid_token(person_project.id_person_creater, authorization)
    if data or not data:
        id_, token = await person_project_storage.create_project(person_project)
        response.headers["Authorization"] = f"Bearer {token}"
        return id_
    raise HTTPException(status_code=422, detail="Не верный токен!")

@router.post("/create-person-project")
async def crate_person_project(person_project: PersonProjectRequest,
        role: str = Depends(get_current_user_role)) -> int:
    if role == "admin":
        id_ = await person_project_storage.create_person_project(person_project)
        return id_
    raise HTTPException(status_code=422, detail="Не верный токен!")

@router.patch("/person-project")
async def update_person_project(person_project: UpdateAccessRightRequest,
        role: str = Depends(get_current_user_role)) -> PersonProjectResponse:
    if role == "admin":
        return await person_project_storage.update_person_project(person_project)
    raise HTTPException(status_code=422, detail="Не верный токен!")

@router.delete("/person-project")
async def delete_person_project(id_project: int, id_person: int,
        role: str = Depends(get_current_user_role)) -> bool:
    if role == "admin":
        return await person_project_storage.delete_person_project_by_person(id_person, id_project)
    raise HTTPException(status_code=422, detail="Не верный токен!")

@router.delete("/project")
async def delete_project(id_project: int, id_person_delete: int,
        role: str = Depends(get_current_user_role),
        sub: str = Depends(get_current_user_sub)) -> bool:
    if role == "admin" and sub == str(id_person_delete):
        return await person_project_storage.delete_person_project_by_project(id_project)
    raise HTTPException(status_code=422, detail="Не верный токен!")

@router.get("/valid-token")
async def valid_token_(
    id_person: int, name_role: str,
    id_project: int,
    role: str = Depends(get_current_user_role),
    sub: str = Depends(get_current_user_sub),
    id_project_token: str = Depends(get_current_user_id_project)):
    if sub != str(id_person):
        raise HTTPException(status_code=401, detail="ID не совпадают")
    if str(id_project) != id_project_token:
        raise HTTPException(status_code=401, detail="ID проектов не совпадают")
    if role == name_role:
        return True
    return False


