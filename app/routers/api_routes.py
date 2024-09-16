from fastapi import APIRouter
from app.routers.auth import router as auth_router
from app.routers.projects import router as projects_router
from app.routers.encryption_routes import router as encryption_router
from app.routers.decryption_routes import router as decryption_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(encryption_router)
router.include_router(decryption_router)
router.include_router(projects_router, prefix="/projects", tags=["projects"])