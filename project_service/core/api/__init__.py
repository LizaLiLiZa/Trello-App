# api/__init__.py
from fastapi import APIRouter
from .project import router as project_router
from .state import router as state_router
from .board import router as board_router
from .task import router as task_router
from .task_categories import router as task_categories_router
from .task_mean import router as task_mean_router
from .delete import router as delete_router

# Создаем главный роутер с префиксом '/api'
router = APIRouter(prefix="/api")

# Подключаем роутеры к главному роутеру
router.include_router(project_router)
router.include_router(state_router)
router.include_router(board_router)
router.include_router(task_router)
router.include_router(task_categories_router)
router.include_router(task_mean_router)
router.include_router(delete_router)
