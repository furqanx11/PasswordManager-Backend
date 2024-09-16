from app.crud.crud import CRUD
from app.schemas.role_schema import RoleCreate, RoleRead, RoleUpdate
from app.routers.routes import routes
from app.models import Roles, Role_Pydantic


role = CRUD(Roles, Role_Pydantic)

router = routes(
    create_func=role.create,
    get_func=role.get,
    update_func=role.update,
    delete_func=role.delete,
    get_all = role.get_all,
    create_schema=RoleCreate,
    response_schema=RoleRead,
    update_schema=RoleUpdate,
    pydantic_model=Role_Pydantic
)