from app.crud.crud import CRUD
from app.schemas.project_schema import ProjectCreate, ProjectRead,ProjectUpdate
from app.routers.routes import routes
from app.models import Project, Project_Pydantic
from app.dependencies.auth import is_admin

project = CRUD(Project, Project_Pydantic)

router = routes(
    create_func=project.create,
    get_func=project.get,
    update_func=project.update,
    delete_func=project.delete,
    create_schema=ProjectCreate,
    response_schema=ProjectRead,
    update_schema=ProjectUpdate
)