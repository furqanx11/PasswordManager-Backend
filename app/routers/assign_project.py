from app.crud.crud import CRUD
from app.schemas.userproject_schema import UserProjectCreate, UserProjectRead,UserProjectUpdate
from app.routers.routes import routes
from app.models import UserProjects, UserProject_Pydantic
from app.models import Projects, Users
from app.schemas.userproject_schema import UserProjectCreate, UserProjectRead, UserProjectUpdate
from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError

project = CRUD(UserProjects, UserProject_Pydantic)

router_new = APIRouter()

@router_new.post("/assign", status_code=status.HTTP_201_CREATED)
async def assign_project_to_users(project_assignment: UserProjectCreate):
    try:
        project = await Projects.get(id=project_assignment.project_id)
       
        users = await Users.filter(id__in=project_assignment.user_id)
        if len(users) != len(project_assignment.user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more users not found")
        existing_assignments = await UserProjects.filter(
            project_id=project_assignment.project_id,
            user_id__in=project_assignment.user_id
        ).values_list('user_id', flat=True)

        new_user_id = [user_id for user_id in project_assignment.user_id if user_id not in existing_assignments]

        if not new_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project is already assigned to all specified users"
            )
        
        for user_id in new_user_id:
            await UserProjects.create(user_id=user_id, project_id=project_assignment.project_id)
        
        return {"message": "Project assigned to users successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate project assignment detected")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# @router_new.post("/assign", status_code=status.HTTP_201_CREATED)
# async def assign_project_to_users(project_assignment: UserProjectCreate):
#     try:
#         project = await Projects.get(id=project_assignment.project_id)
        
#         # Fetch the "admin" user
#         admin_user = await Users.get(username="admin")
        
#         # Ensure the "admin" user exists
#         if not admin_user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found")
        
#         # Assign the project to the "admin" user if not already assigned
#         admin_assignment = await UserProjects.filter(
#             project_id=project_assignment.project_id,
#             user_id=admin_user.id
#         ).exists()
        
#         if not admin_assignment:
#             await UserProjects.create(user_id=admin_user.id, project_id=project_assignment.project_id)
        
#         users = await Users.filter(id__in=project_assignment.user_id)
#         if len(users) != len(project_assignment.user_id):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more users not found")
        
#         existing_assignments = await UserProjects.filter(
#             project_id=project_assignment.project_id,
#             user_id__in=project_assignment.user_id
#         ).values_list('user_id', flat=True)

#         new_user_id = [user_id for user_id in project_assignment.user_id if user_id not in existing_assignments]

#         if not new_user_id:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Project is already assigned to all specified users"
#             )
        
#         for user_id in new_user_id:
#             await UserProjects.create(user_id=user_id, project_id=project_assignment.project_id)
        
#         return {"message": "Project assigned to users successfully"}
#     except DoesNotExist:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
#     except IntegrityError:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate project assignment detected")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

router = routes(
    create_func=project.create,
    get_func=project.get,
    update_func=project.update,
    delete_func=project.delete,
    get_all = project.get_all,
    create_schema=UserProjectCreate,
    response_schema=UserProjectRead,
    update_schema=UserProjectUpdate,
    pydantic_model=UserProject_Pydantic,
    model_name="ASSIGN_PROJECT"
)