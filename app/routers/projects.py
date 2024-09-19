from app.crud.crud import CRUD
from app.schemas.project_schema import ProjectCreate, ProjectRead,ProjectUpdate
from app.routers.routes import routes
from app.models import Projects, Project_Pydantic

project = CRUD(Projects, Project_Pydantic)

router = routes(
    create_func=project.create,
    get_func=project.get,
    update_func=project.update,
    delete_func=project.delete,
    get_all = project.get_all,
    create_schema=ProjectCreate,
    response_schema=ProjectRead,
    update_schema=ProjectUpdate,
    pydantic_model=Project_Pydantic,
    model_name="PROJECT"
)