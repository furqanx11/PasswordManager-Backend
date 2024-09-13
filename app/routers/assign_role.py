from app.crud.crud import CRUD
from app.schemas.user_role_schema import UserRoleCreate, UserRoleRead, UserRoleUpdate
from app.routers.routes import routes
from app.models import UserRoles, UserRole_Pydantic

user_role = CRUD(UserRoles, UserRole_Pydantic)

router = routes(
    create_func=user_role.create,
    get_func=user_role.get,
    update_func=user_role.update,
    delete_func=user_role.delete,
    create_schema=UserRoleCreate,
    response_schema=UserRoleRead,
    update_schema=UserRoleUpdate
)