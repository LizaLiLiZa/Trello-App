from fastapi import APIRouter, Header, HTTPException
from ..storage import access_right_storage

from ..models.access_right.request import AccessRightsRequest

from ..models.access_right.response import AccessRightsResponse
from ..services.auth.valid_token import valid_token

router = APIRouter(tags=["Access Right"])

@router.get("/access-right")
async def get_access_right(id_person: int, authorization: str = Header(None)) -> list[AccessRightsResponse]:
    data = await valid_token(id_person, authorization)
    if not data:
        return await access_right_storage.get_access_right()
    raise HTTPException(status_code=403, detail="Упс, недостаточный уровень доступа!")

@router.post("/access-right")
async def create_access_right(access_rights: AccessRightsRequest, id_person: int, authorization: str = Header(None)) -> int:
    data = await valid_token(id_person, authorization)
    if not data:
        return await access_right_storage.create_access_right(access_rights)
    raise HTTPException(status_code=403, detail="Упс, недостаточный уровень доступа!")

@router.delete("/access-right")
async def delete_access_rights(id_:int, id_person: int, authorization: str = Header(None)) -> bool:
    data = await valid_token(id_person, authorization)
    if not data:
        return await access_right_storage.delete_acces_right(id_)
    raise HTTPException(status_code=403, detail="Упс, недостаточный уровень доступа!")
