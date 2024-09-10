from fastapi import APIRouter
from app.routers.auth import router as auth_router
from app.routers.projects import router as projects_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(projects_router, prefix="/projects", tags=["projects"])