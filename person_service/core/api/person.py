from fastapi import APIRouter, Response, Depends, HTTPException
from ..models.person.request import CreatePersonRequest
from ..models.person.response import PersonResponse
from ..models.person.response import PersonInfoResponse
from ..models.person.request import GetOnePersonRequest
from ..models.person.request import PersonInfoRequest
from ..models.person.request import PersonPasswordRequest
from ..storage import person_storage
from ..services.auth.auth_utils import get_current_user_role
from ..services.auth.auth_utils import get_current_user_sub


router = APIRouter()

@router.post("/person")
async def create_person(person: CreatePersonRequest) -> int:
    return await person_storage.create_person(person)

@router.get("/person", response_model = PersonResponse)
async def get_one_person(password: str, login: str, response: Response):
    person, token =  await person_storage.login(GetOnePersonRequest(password=password, login=login))
    response.headers["Authorization"] = f"Bearer {token.access_token}"
    return person

@router.get("/person-info", response_model = PersonInfoResponse)
async def get_person_info(id_: int,
    role: str = Depends(get_current_user_role)):
    if role != "admin" and role != "user":
        raise HTTPException(status_code=401, detail="Нет прав доступа!")
    return await person_storage.get_one_person(id_)

@router.get("/persons", response_model=list[PersonResponse])
async def get_all_persons(
    role: str = Depends(get_current_user_role)
):
    if role != "admin":
        raise HTTPException(status_code=401, detail="Нет прав доступа!")
    return await person_storage.get_all_persons()

@router.put("/person/info", response_model = PersonResponse)
async def update_person(
    person: PersonInfoRequest,
    role: str = Depends(get_current_user_role),
    sub: str = Depends(get_current_user_sub)
    ):
    if not role in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Неверная роль!")
    if sub != str(person.id):
        raise HTTPException(status_code=403, detail="Неверный id пользователя!")

    return await person_storage.update_person(person)

@router.put("/person/password", response_model = PersonResponse)
async def update_password_person(person:PersonPasswordRequest,
    sub: str = Depends(get_current_user_sub)):
    print(1)
    if str(person.id) != sub:
        raise HTTPException(status_code=401, detail="Нет прав доступа!")
    return await person_storage.update_password_person(person)

# @router.patch("/person", response_model = str)
# async def update_person_del(person: GetOnePersonRequest):
#     return await person_storage.update_person_del(person)

# @router.delete("/person_admin", response_model = str)
# async def delete_person_admin(person: IdRequest):
#     return await person_storage.delete_person_admin(person)

@router.get("/valid-token")
async def valid_token(
    id_person: int,
    role: str = Depends(get_current_user_role),
    sub: str = Depends(get_current_user_sub)):
    if sub != str(id_person):
        raise HTTPException(status_code=401, detail="ID не совпадают")
    if "admin" != role:
        return True
    return False

# {
#   "first_name": "Елизавета",
#   "last_name": "Гурченкова",
#   "middle_name": "Владимировна",
#   "birthday_at": "2005-02-26",
#   "phone": 88005553535,
#   "email": "user@example.com",
#   "password": "qwe123rty"
# }