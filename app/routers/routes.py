from fastapi import APIRouter, HTTPException, status, Depends
from typing import Type, TypeVar, Callable
from pydantic import BaseModel, ValidationError
from app.exceptions.custom_exceptions import CustomValidationException
from app.middleware.permissions import permission_dependency
from typing import List, Any
from app.models import Projects, Users, Roles, Permissions
from app.schemas.role_permission_schema import RolePermissionCreate
from app.schemas.userproject_schema import UserProjectCreate
from app.utils.assignment_functions import assign_permissions, assign_project_to_users
from app.dependencies.auth import get_current_user

TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TResponseSchema = TypeVar("TResponseSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)

def routes(
    create_func: Callable[[dict], TResponseSchema],
    get_func: Callable[[str], TResponseSchema],
    get_all : Callable[[], list[Any]],
    update_func: Callable[[str, dict], TResponseSchema],
    delete_func: Callable[[str], None],
    create_schema: Type[TCreateSchema],
    response_schema: Type[TResponseSchema],
    update_schema: Type[TUpdateSchema],
    pydantic_model: Type = None,
    model_name: str = "MODEL",
) -> APIRouter:
    router = APIRouter() 


    @router.post("/", response_model=pydantic_model, status_code=status.HTTP_201_CREATED, dependencies=[Depends(permission_dependency(f"{model_name}:CREATE"))])
    async def create(item: create_schema, current_user: Users = Depends(get_current_user)):
            try:
                item = await create_func(item.dict())
                if not item:
                    raise CustomValidationException(status_code=400, detail="Item not created.", pre = True)
                if model_name == 'PROJECT':
                    project = await Projects.get_or_none(name=item.name)
                    admin = await Users.get_or_none(username="admin")
                    if admin.id != current_user['id']:
                        project_assignment_data = UserProjectCreate(
                            project_id= project.id,  
                            user_id=[current_user['id'], admin.id]
                        )
                    else:
                        project_assignment_data = UserProjectCreate(
                            project_id= project.id,  
                            user_id=[current_user['id']]
                        )
                    await assign_project_to_users(project_assignment_data)

                elif model_name == 'PERMISSION':
                     permission = await Permissions.get_or_none(name=item.name)
                     role = await Roles.get_or_none(name="admin")
                     permission_assignment_data = RolePermissionCreate(
                            permission_id=[permission.id],
                            role_id=role.id
                        )
                     await assign_permissions(permission_assignment_data)

                return item
            except ValidationError as e:
                raise CustomValidationException(status_code=400, detail=str(e))

    @router.get("/", response_model=List[response_schema], dependencies=[Depends(permission_dependency(f"{model_name}:GET:ALL"))])
    async def read_all():
            items = await get_all()
            return items

    @router.get("/{id}", response_model=response_schema, dependencies=[Depends(permission_dependency(f"{model_name}:GET"))])
    async def read(id: str):
            item = await get_func(id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item

    @router.patch("/{id}", response_model=pydantic_model, dependencies=[Depends(permission_dependency(f"{model_name}:UPDATE"))])
    async def update_item(id: str, item: update_schema):
            try:
                item_data = item.dict(exclude_unset=True)
                updated_item = await update_func(id, item_data)
                if not updated_item:
                    raise HTTPException(status_code=404, detail="Item not found")
                return updated_item
            except ValidationError as e:
                raise HTTPException(status_code=422, detail=str(e))
            
    @router.delete("/{id}", response_model=dict, dependencies=[Depends(permission_dependency(f"{model_name}:DELETE"))])
    async def delete(id: str):
            item_to_delete = await get_func(id)
            if not item_to_delete:
                raise HTTPException(status_code=404, detail="Item not found")
            await delete_func(id)
            return {"detail": "Item deleted successfully"}

    return router

