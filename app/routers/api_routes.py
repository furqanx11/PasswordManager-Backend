from fastapi import APIRouter, FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import projects, assign_project, user, roles, permissions, modes, fields, assign_permission, assign_role

app = FastAPI()

router = APIRouter()

router.include_router(user.router)
router.include_router(projects.router, prefix="/project", tags=["projects"])
router.include_router(assign_project.router, prefix="/assign_project", tags=["assign_projects"])
router.include_router(assign_project.router_new, prefix="/assign_project", tags=["assign_projects"])
router.include_router(roles.router, prefix="/role", tags=["roles"])
router.include_router(roles.router_new, prefix="/role", tags=["roles"])
router.include_router(assign_permission.router, prefix="/assign_permission", tags=["assign_permissions"])
router.include_router(permissions.router, prefix="/permission", tags=["permissions"])
router.include_router(assign_permission.router_new, prefix="/assign_permission", tags=["assign_permissions"])
router.include_router(modes.router, prefix="/mode", tags=["modes"])
router.include_router(fields.router, prefix="/field", tags=["fields"])
router.include_router(assign_role.router, prefix="/assign_role", tags=["assign_role"])
router.include_router(assign_role.router_new, prefix="/assign_role", tags=["assign_role"])