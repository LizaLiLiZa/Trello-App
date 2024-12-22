from fastapi import APIRouter

from ..storage import state_storage

from ..models.states.request import StateRequest
from ..models.states.response import StateResponse

router = APIRouter(tags=["State"])

@router.post("/state")
async def create_state(state: StateRequest) -> list[StateResponse]:
    return await state_storage.create_state(state)

@router.get("/states")
async def get_states(id_board: int) -> list[StateResponse]:
    return await state_storage.get_states(id_board)

@router.patch("/state")
async def update_state(state: StateRequest) -> list[StateResponse]:
    return await state_storage.update_states(state)
