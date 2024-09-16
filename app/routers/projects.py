from app.crud.crud import CRUD
from app.schemas.project_schema import ProjectCreateSchema, ProjectReadSchema,ProjectUpdateSchema
from app.routers.routes import routes
from app.models import Projects, Project_Pydantic
from app.dependencies.auth import is_admin

project = CRUD(Projects, Project_Pydantic)

router = routes(
    create_func=project.create,
    get_func=project.get,
    update_func=project.update_partial,
    delete_func=project.delete,
    create_schema=ProjectCreateSchema,
    response_schema=ProjectReadSchema,
    update_schema=ProjectUpdateSchema,
    is_admin = is_admin
)