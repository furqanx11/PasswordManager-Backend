from sqlite3 import IntegrityError
from app.crud.crud import CRUD
from app.schemas.role_permission_schema import RolePermissionCreate, RolePermissionRead, RolePermissionUpdate
from app.routers.routes import routes
from app.models import RolePermissions, RolePermission_Pydantic, Permissions, Roles
from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import DoesNotExist
from typing import List

role_permission = CRUD(RolePermissions, RolePermission_Pydantic, related_fields=['role', 'permission'])

router_new = APIRouter()


@router_new.post("/assign", response_model=List[RolePermissionRead], status_code=status.HTTP_201_CREATED)
async def assign_permissions(role_permission: RolePermissionCreate):
    try:
        # Check if the role exists
        role = await Roles.get(id=role_permission.role_id)
        
        # Normalize permission_id to a list
        if isinstance(role_permission.permission_id, int):
            permission_ids = [role_permission.permission_id]
        else:
            permission_ids = role_permission.permission_id

        # Check if all permissions exist
        permissions = await Permissions.filter(id__in=permission_ids)
        if len(permissions) != len(permission_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more permissions not found")

        # Check if the role already has the specified permissions
        existing_permissions = await RolePermissions.filter(
            role_id=role_permission.role_id,
            permission_id__in=permission_ids
        ).values_list('permission_id', flat=True)

        # Filter out already assigned permissions
        new_permissions = [perm_id for perm_id in permission_ids if perm_id not in existing_permissions]

        if not new_permissions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All specified permissions are already assigned to the role"
            )

        # Assign only the new permissions
        created_permissions = []
        for permission_id in new_permissions:
            created_permission = await RolePermissions.create(role_id=role_permission.role_id, permission_id=permission_id)
            created_permissions.append(created_permission)

        # Convert the created RolePermissions instances to RolePermissionRead models
        created_permissions_read = [RolePermissionRead.from_orm(perm) for perm in created_permissions]

        return created_permissions_read
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate permission assignment detected")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


router = routes(
    create_func=role_permission.create,
    get_func=role_permission.get,
    update_func=role_permission.update,
    delete_func=role_permission.delete,
    get_all = role_permission.get_all,
    create_schema=RolePermissionCreate,
    response_schema=RolePermissionRead,
    update_schema=RolePermissionUpdate,
    pydantic_model=RolePermission_Pydantic,
    model_name="ASSIGN_PERMISSION"
)