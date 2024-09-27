from app.crud.crud import CRUD
from app.schemas.user_role_schema import UserRoleCreate, UserRoleRead, UserRoleUpdate
from app.routers.routes import routes
from app.models import UserRoles, UserRole_Pydantic, Users, Roles
from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import DoesNotExist

user_role = CRUD(UserRoles, UserRole_Pydantic, related_fields=['user', 'role'])

router_new = APIRouter()

@router_new.post("/assign", status_code=status.HTTP_201_CREATED)
async def assign_roles(role_assignment: UserRoleCreate):
    try:
        # Check if the user exists
        user = await Users.get(id=role_assignment.user_id)
        
        # Check if all roles exist
        roles = await Roles.filter(id__in=role_assignment.role_id)
        if len(roles) != len(role_assignment.role_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more roles not found")

        # Assign roles to the user
        for role_id in role_assignment.role_id:
            await UserRoles.create(user_id=role_assignment.user_id, role_id=role_id)
        
        return {"message": "Roles assigned successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

router = routes(
    create_func=user_role.create,
    get_func=user_role.get,
    update_func=user_role.update,
    delete_func=user_role.delete,
    get_all = user_role.get_all,
    create_schema=UserRoleCreate,
    response_schema=UserRoleRead,
    update_schema=UserRoleUpdate,
    pydantic_model=UserRole_Pydantic,
    model_name="ASSIGN_ROLE"
)