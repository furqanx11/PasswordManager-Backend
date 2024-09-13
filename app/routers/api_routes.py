from fastapi import APIRouter
from app.routers import projects, assign_project, user, roles, permissions, modes, fields, assign_permission

router = APIRouter()

router.include_router(user.router)
router.include_router(projects.router, prefix="/project", tags=["projects"])
router.include_router(assign_project.router, prefix="/assign_project", tags=["assign_projects"])
router.include_router(roles.router, prefix="/role", tags=["roles"])
router.include_router(permissions.router, prefix="/permission", tags=["permissions"])
router.include_router(assign_permission.router, prefix="/assign_permission", tags=["assign_permissions"])
router.include_router(modes.router, prefix="/mode", tags=["modes"])
router.include_router(fields.router, prefix="/field", tags=["fields"])