from fastapi import APIRouter

from ..storage import board_storage
from ..models.boards.requests import BoardRequest
from ..models.boards.responses import BoardResponse

from ..service.auth.valid_token import valid_token_person
from ..service.auth.valid_token import valid_token_person_project

router = APIRouter(tags=["Board"])

@router.get("/boards")
async def get_boards(id_project: int) -> list[BoardResponse]:
    return await board_storage.get_board(id_project)

@router.get("/board")
async def get_board(id_board: int) -> BoardResponse:
    return await board_storage.get_board_by_id(id_board)

@router.post("/board")
async def create_board(board: BoardRequest): # -> list[BoardResponse]:
    return await board_storage.create_board(board)

@router.patch("/board")
async def upgrade_board(board: BoardResponse) -> BoardResponse:
    return await board_storage.update_board(board)
