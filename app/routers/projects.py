from app.crud.crud import CRUD
from app.schemas.project_schema import ProjectCreate, ProjectRead,ProjectUpdate
from app.routers.routes import routes
from app.models import Projects, Project_Pydantic, UserProjects
from fastapi import APIRouter, HTTPException, Depends, status
from app.middleware.permissions import permission_dependency
from tortoise.exceptions import DoesNotExist
from app.schemas.user_schema import UserRead, ProjectUsers

project = CRUD(Projects, Project_Pydantic)

router_new = APIRouter()
@router_new.get("/{project_id}/users", response_model=ProjectUsers, status_code=status.HTTP_200_OK, dependencies=[Depends(permission_dependency("VIEW_PROJECT_USERS"))])
async def get_users_assigned_to_project(project_id: int):
    try:
        project = await Projects.get_or_none(id=project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        user_projects = await UserProjects.filter(project_id=project_id).prefetch_related('user')
        users = [user_project.user for user_project in user_projects]

        return ProjectUsers(
            project_id=project_id,
            users=[UserRead.from_orm(user) for user in users]
        )
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    except Exception as e:
        #logger.error(f"Error fetching users for project {project_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
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