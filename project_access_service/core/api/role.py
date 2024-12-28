from fastapi import APIRouter, Depends, HTTPException

from ..storage import role_storage

from ..models.roles.request import ProjectRolesRequest

from ..models.roles.response import ProjectRolesResponse

from ..services.auth.auth_utils import get_current_user_role
from ..services.auth.auth_utils import get_current_user_id_project

router = APIRouter(tags=["Role"])

@router.get("/roles")
async def get_roles(id_project: int,
        id_project_token: str = Depends(get_current_user_id_project)) -> list[ProjectRolesResponse]:
    if str(id_project) == id_project_token:
        return await role_storage.get_roles(id_project)
    raise HTTPException(status_code=403, detail="Нет доступа!")

@router.post("/role")
async def create_role(role: ProjectRolesRequest,
        id_project_token: str = Depends(get_current_user_id_project),
        role_token: str = Depends(get_current_user_role)) -> int:
    if role_token in ["admin", "editing"] and id_project_token == str(role.id_project):
        return await role_storage.create_role(role)
    raise HTTPException(status_code=403, detail="Нет доступа!")

@router.delete("/role")
async def delete_role(id_role: int,
        id_project_token: str = Depends(get_current_user_id_project),
        role_token: str = Depends(get_current_user_role)) -> bool:
    role = role_storage.get_role(id_role)
    if str(role.id_project) == id_project_token and role_token in ["admin", "editing"]:
        return await role_storage.delete_roles_by_id(id_role)
    raise HTTPException(status_code=403, detail="Нет доступа!")
