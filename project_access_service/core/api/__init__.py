# api/__init__.py
from fastapi import APIRouter
from .access_right import router as access_right_router
from .role import router as role_router
from .person_project_role import router as person_project_role_router
from .person_project import router as person_project_router

router = APIRouter(prefix="/api")

router.include_router(access_right_router)
router.include_router(role_router)
router.include_router(person_project_role_router)
router.include_router(person_project_router)
