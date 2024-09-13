from app.crud.crud import CRUD
from app.schemas.permission_schema import PermissionCreate, PermissionRead, PermissionUpdate
from app.routers.routes import routes
from app.models import Permission, Permission_Pydantic

permission = CRUD(Permission, Permission_Pydantic)

router = routes(
    create_func=permission.create,
    get_func=permission.get,
    update_func=permission.update,
    delete_func=permission.delete,
    create_schema=PermissionCreate,
    response_schema=PermissionRead,
    update_schema=PermissionUpdate
)