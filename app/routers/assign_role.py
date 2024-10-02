from app.crud.crud import CRUD
from app.schemas.user_role_schema import UserRoleCreate, UserRoleRead, UserRoleUpdate
from app.routers.routes import routes
from app.models import UserRoles, UserRole_Pydantic, Users, Roles
from fastapi import APIRouter, HTTPException, status, Depends
from tortoise.exceptions import DoesNotExist
from app.middleware.permissions import permission_dependency
from tortoise.exceptions import DoesNotExist, IntegrityError

user_role = CRUD(UserRoles, UserRole_Pydantic, related_fields=['user', 'role'])

router_new = APIRouter()

@router_new.post("/assign", status_code=status.HTTP_201_CREATED, dependencies=[Depends(permission_dependency("ASSIGN_ROLE:CREATE"))])
async def assign_roles(role_assignment: UserRoleCreate):
    try:
        user = await Users.get(id=role_assignment.user_id)
        
        roles = await Roles.filter(id__in=role_assignment.role_id)
        if len(roles) != len(role_assignment.role_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more roles not found")

        for role_id in role_assignment.role_id:
            await UserRoles.create(user_id=role_assignment.user_id, role_id=role_id)
        
        return {"message": "Roles assigned successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router_new.put("/update", status_code=status.HTTP_200_OK, dependencies=[Depends(permission_dependency("ASSIGN_ROLE:UPDATE"))])
async def update_user_roles(user_role_update: UserRoleUpdate):
    try:
        user = await Users.get(id=user_role_update.user_id)
        
        roles = await Roles.filter(id__in=user_role_update.role_id)
        if len(roles) != len(user_role_update.role_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more roles not found")

        await UserRoles.filter(user_id=user_role_update.user_id).delete()
        created_assignments = []
        for role_id in user_role_update.role_id:
            created_assignment = await UserRoles.create(user_id=user_role_update.user_id, role_id=role_id)
            created_assignments.append(created_assignment)

        return {"message": "User roles updated successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate role assignment detected")
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