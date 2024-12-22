from fastapi import APIRouter
from ..models.person.request import CreatePersonRequest
from ..models.person.response import PersonResponse
from ..models.person.request import GetOnePersonRequest
from ..models.person.request import IdRequest
from ..models.person.request import PersonInfoRequest
from ..models.person.request import PersonPasswordRequest
from ..storage import person_storage

router = APIRouter()

@router.post("/person", response_model = PersonResponse)
async def create_person(person: CreatePersonRequest):
    return await person_storage.create_person(person)

@router.get("/person", response_model = PersonResponse)
async def get_one_person(password: str, login: str):
    return await person_storage.get_one_person(GetOnePersonRequest(password=password, login=login))

@router.get("/persons", response_model=list[PersonResponse])
async def get_all_persons():
    return await person_storage.get_all_persons()

@router.put("/person/info", response_model = PersonResponse)
async def update_person(person: PersonInfoRequest):
    return await person_storage.update_person(person)

@router.put("/person/password", response_model = PersonResponse)
async def update_password_person(person:PersonPasswordRequest):
    return await person_storage.update_password_person(person)

@router.patch("/person", response_model = str)
async def update_person_del(person: GetOnePersonRequest):
    return await person_storage.update_person_del(person)

@router.delete("/person_admin", response_model = str)
async def delete_person_admin(person: IdRequest):
    return await person_storage.delete_person_admin(person)
