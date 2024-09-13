from app.crud.crud import CRUD
from app.schemas.userproject_schema import UserProjectCreate, UserProjectRead,UserProjectUpdate
from app.routers.routes import routes
from app.models import UserProjects, UserProject_Pydantic
from app.dependencies.auth import is_admin

project = CRUD(UserProjects, UserProject_Pydantic)

router = routes(
    create_func=project.create,
    get_func=project.get,
    update_func=project.update,
    delete_func=project.delete,
    create_schema=UserProjectCreate,
    response_schema=UserProjectRead,
    update_schema=UserProjectUpdate
)