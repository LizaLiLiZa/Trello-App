from fastapi import APIRouter

from ..storage import delete_storage

router = APIRouter(tags=["Delete"])

@router.delete("/task")
async def delete_task(id_task: int) -> bool:
    return await delete_storage.delete_task(id_task)

@router.delete("/state")
async def delete_state(id_state: int) -> bool:
    return await delete_storage.delete_state(id_state)

@router.delete("/board")
async def delete_board(id_board: int) -> bool:
    return await delete_storage.delete_board(id_board)


@router.delete("/project")
async def delete_project(id_project: int) -> bool:
    return await delete_storage.delete_project(id_project)


@router.delete("/person")
async def delete_persons(id_persons: int) -> bool:
    return await delete_storage.delete_person(id_persons)

