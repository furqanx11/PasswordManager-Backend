from app.crud.crud import CRUD
from app.schemas.role_schema import RoleCreate, RoleRead, RoleUpdate
from app.routers.routes import routes
from app.models import Roles, Role_Pydantic
from app.models import RolePermissions
from app.schemas.permission_schema import RolePermissionResponse
from app.schemas.permission_schema import PermissionRead
from fastapi import APIRouter, HTTPException, status, Depends
from tortoise.exceptions import DoesNotExist
from app.middleware.permissions import permission_dependency


role = CRUD(Roles, Role_Pydantic)

router_new = APIRouter()

@router_new.get("/{role_id}/permissions", response_model=RolePermissionResponse, dependencies=[Depends(permission_dependency("ROLE:PERMISSIONS"))])
async def get_permissions_for_role(role_id: int):
    try:
        role = await Roles.get(id=role_id)
        
        role_permissions = await RolePermissions.filter(role_id=role_id).prefetch_related('permission')
        permissions = [PermissionRead.from_orm(rp.permission) for rp in role_permissions]
        
        return RolePermissionResponse(role_id=role_id, permissions=permissions)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


router = routes(
    create_func=role.create,
    get_func=role.get,
    update_func=role.update,
    delete_func=role.delete,
    get_all = role.get_all,
    create_schema=RoleCreate,
    response_schema=RoleRead,
    update_schema=RoleUpdate,
    pydantic_model=Role_Pydantic,
    model_name="ROLE"
)