from fastapi import APIRouter, Depends, HTTPException

from ..storage import person_project_role_storage

from ..storage import person_project_storage

from ..models.person_project_role.request import PersonProjectRolesRequest

from ..models.person_project_role.response import PersonProjectRolesResponse

from ..services.auth.auth_utils import get_current_user_role
from ..services.auth.auth_utils import get_current_user_id_project

router = APIRouter(tags=["Person Project Role"])

@router.get("/person-project-role")
async def get_info(id_person_project: int, id_project: int,
            id_project_token: str = Depends(get_current_user_id_project),
            ) -> list[PersonProjectRolesResponse]:
    if str(id_project) == id_project_token:
        return await person_project_role_storage.get_person_project_role(id_person_project)
    raise HTTPException(status_code=403, detail="Упс, у вас нет прав доступа!")

@router.post("/person-project-role")
async def create_info(person_project_role: PersonProjectRolesRequest,
        role: str = Depends(get_current_user_role),
        id_project: str = Depends(get_current_user_id_project)) -> int:
    if role in ["editing", "admin"] and id_project == person_project_role.id_project:
        return await person_project_role_storage.create_person_project_role(person_project_role)
    raise HTTPException(status_code=403, detail="Упс, у вас нет прав доступа!")

@router.delete("/person-project-roles")
async def delete_info(id_person_project: int,
        role: str = Depends(get_current_user_role),
        id_project: str = Depends(get_current_user_id_project)) -> bool:
    data = await person_project_storage.get_persons_project_by_id(id_person_project)
    if role == "admin" and id_project == str(data.id_project):
        return await person_project_role_storage.delete_person_project_role_by_person_project(id_person_project)
    raise HTTPException(status_code=403, detail="Упс, у вас нет прав доступа!")

@router.delete("/person-project-role")
async def delete_person_project_role(id_person_project_role: int,
        role: str = Depends(get_current_user_role),
        id_project: str = Depends(get_current_user_id_project)) -> bool:
    person_project_role = await person_project_role_storage.get_person_project_role_id(id_person_project_role)
    person_project = await person_project_storage.get_persons_project_by_id(person_project_role.id_person_project)
    if role == "admin" and id_project == str(person_project.id_project):
        return await person_project_role_storage.delete_person_project_role_by_id(id_person_project_role)
    raise HTTPException(status_code=403, detail="Упс, у вас нет прав доступа!")

