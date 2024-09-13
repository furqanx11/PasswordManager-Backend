from app.crud.crud import CRUD
from app.schemas.role_permission_schema import RolePermissionCreate, RolePermissionRead, RolePermissionUpdate
from app.routers.routes import routes
from app.models import RolePermissions, RolePermission_Pydantic

role_permission = CRUD(RolePermissions, RolePermission_Pydantic)

router = routes(
    create_func=role_permission.create,
    get_func=role_permission.get,
    update_func=role_permission.update,
    delete_func=role_permission.delete,
    create_schema=RolePermissionCreate,
    response_schema=RolePermissionRead,
    update_schema=RolePermissionUpdate
)