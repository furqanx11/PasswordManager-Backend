from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.models import Users, User_Pydantic, UserRoles, Role_Pydantic, RolePermissions,Permission_Pydantic, Roles, Permissions
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from app.schemas.project_schema import ProjectWithFields
from app.utils.jwt import create_access_token, verify_password, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from app.dependencies.auth import get_current_user
from app.crud.crud import CRUD
from typing import List
from app.models import UserProjects, Project_Pydantic,Field_Pydantic, Fields
from app.middleware.permissions import permission_dependency, has_permission
from tortoise.transactions import in_transaction
from app.routers.fields import get_fields_by_mode
import logging

router = APIRouter()
user_crud = CRUD(Users, User_Pydantic)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate):
    try:
        user_obj = await Users.create(
            name = user.name,
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password)
        )
        return await User_Pydantic.from_tortoise_orm(user_obj)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await Users.get_or_none(username=form_data.username)  
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(user)  
        
        response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=1800)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/me", response_model=UserUpdate)
async def update_user_me(user_update: UserUpdate, current_user: Users = Depends(get_current_user)):
        async with in_transaction():
            # Fetch the current user from the database
            current_user = await Users.get(id=current_user['id'])
            # Update only the fields that are provided in the request
            if user_update.name is not None:
                current_user.name = user_update.name
            if user_update.username is not None:
                current_user.username = user_update.username
            if user_update.email is not None:
                current_user.email = user_update.email
            if user_update.password is not None:
                current_user.password = get_password_hash(user_update.password)

            # Save the updated user
            await current_user.save()

            return await User_Pydantic.from_tortoise_orm(current_user)

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    print(current_user)
    print(current_user['username'])
    return await user_crud.get_by_username(username=current_user["username"])

@router.get("/users", response_model=list[UserRead], dependencies=[Depends(permission_dependency("USER:LIST"))])
async def get_all_users():
    users = Users.all()
    return await User_Pydantic.from_queryset(users)

# @router.get("/me/projects", response_model=List[ProjectWithFields])
# async def get_user_projects(current_user: Users = Depends(get_current_user)):
#     try:
#         user_id = current_user['id']
#         user = await Users.get_or_none(id=user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found.")

#         user_projects = await UserProjects.filter(user_id=user_id).prefetch_related('project')
#         projects = [user_project.project for user_project in user_projects]
#         project_ids = [project.id for project in projects]

#         # Fetch fields as dictionaries
#         fields = await Fields.filter(project_id__in=project_ids).values()

#         fields_by_project = {}
#         for field in fields:
#             if field['project_id'] not in fields_by_project:
#                 fields_by_project[field['project_id']] = []
#             fields_by_project[field['project_id']].append(field)

#         project_data = []
#         for project in projects:
#             project_dict = await Project_Pydantic.from_tortoise_orm(project)
#             project_dict = project_dict.dict()

#             modes = await has_permission(None, "FIELD:GET:MODE", user_id)
#             if modes == True:
#                 keys = await get_fields_by_mode(None, project.name)
#                 project_dict['fields'] = keys
#             elif "ALL" in modes:
#                 keys = await get_fields_by_mode(None, project.name)
#                 project_dict['fields'] = keys
#             elif modes:
#                 project_dict['fields'] = await get_fields_by_mode(modes, project.name)
    
            
#             project_data.append(project_dict)

#         return project_data
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")

@router.get("/me/projects", response_model=List[ProjectWithFields])
async def get_user_projects(current_user: Users = Depends(get_current_user)):
    try:
        user_id = current_user['id']
        user = await Users.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        user_projects = await UserProjects.filter(user_id=user_id).prefetch_related('project')
        projects = [user_project.project for user_project in user_projects]
        project_ids = [project.id for project in projects]

        # Fetch fields as dictionaries
        fields = await Fields.filter(project_id__in=project_ids).values()

        if not fields:
            # If no fields are found, return only projects
            project_data = [await Project_Pydantic.from_tortoise_orm(project) for project in projects]
            return project_data

        fields_by_project = {}
        for field in fields:
            if field['project_id'] not in fields_by_project:
                fields_by_project[field['project_id']] = []
            fields_by_project[field['project_id']].append(field)

        project_data = []
        for project in projects:
            project_dict = await Project_Pydantic.from_tortoise_orm(project)
            project_dict = project_dict.dict()

            try:
                modes = await has_permission(None, "FIELD:GET:MODE", user_id)
                if modes == True:
                    keys = await get_fields_by_mode(None, project.name)
                    project_dict['fields'] = keys
                elif "ALL" in modes:
                    keys = await get_fields_by_mode(None, project.name)
                    project_dict['fields'] = keys
                elif modes:
                    project_dict['fields'] = await get_fields_by_mode(modes, project.name)
            except HTTPException as e:
                if e.detail == "You do not have the necessary permissions":
                    # If permission error, return only projects
                    project_data = [await Project_Pydantic.from_tortoise_orm(project) for project in projects]
                    return project_data
                else:
                    raise e

            project_data.append(project_dict)

        return project_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")

@router.get("/user/{user_id}", response_model=UserRead, dependencies=[Depends(permission_dependency("USER:GET"))])
async def get_user_by_id(user_id: int):
    try:
        user = await Users.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return await User_Pydantic.from_tortoise_orm(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching user with id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/user/{user_id}", response_model=UserRead, dependencies=[Depends(permission_dependency("USER:UPDATE"))])
async def update_user_by_id(user_id: int, user_update: UserUpdate):
    try:
        user = await Users.get_or_none(id=user_id)
        if not user:
           raise HTTPException(status_code=404, detail="User not found.")
        
        user_data = user_update.dict(exclude_unset=True)
        if 'password' in user_data:
            user_data['password'] = get_password_hash(user_data['password'])
        
        for key, value in user_data.items():
            setattr(user, key, value)
        await user.save()
        return await User_Pydantic.from_tortoise_orm(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating user with id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(permission_dependency("USER:DELETE"))])
async def delete_user_by_id(user_id: int):
    try:
        user = await Users.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        await user.delete()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating user with id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/refresh_token")
async def refresh_token(response: Response, current_user: Users = Depends(get_current_user)):
    try:
        user = await Users.get_or_none(username=current_user['username'])  
        
        access_token_expires = timedelta(minutes=30)
        access_token = await create_access_token(user, expires_delta=access_token_expires)  
        
        response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=1800)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e

@router.get("/me/roles", response_model=List[Role_Pydantic])
async def get_user_roles(current_user: Users = Depends(get_current_user)):
    try:
        user_id = int(current_user['id'])
        user_roles = await UserRoles.filter(user_id=user_id).values()
        role_ids = [user_role['role_id'] for user_role in user_roles]
        roles = await Role_Pydantic.from_queryset(Roles.filter(id__in=role_ids))
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error{str(e)}")
    
@router.get("/user/{user_id}/roles", response_model=List[Role_Pydantic])
async def get_user_roles(user_id: int):
    try:
        user_roles = await UserRoles.filter(user_id=user_id).values()
        role_ids = [user_role['role_id'] for user_role in user_roles]
        roles = await Role_Pydantic.from_queryset(Roles.filter(id__in=role_ids))
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error{str(e)}")
    
@router.get("/me/permissions", response_model=List[Permission_Pydantic])
async def get_user_permissions(current_user: Users = Depends(get_current_user)):
    try:
        user_roles = await UserRoles.filter(user_id=current_user['id']).values()
        role_ids = [user_role['role_id'] for user_role in user_roles]
        role_permissions = await RolePermissions.filter(role_id__in=role_ids).values()
        permission_ids = [role_permission['permission_id'] for role_permission in role_permissions]
        permissions = await Permission_Pydantic.from_queryset(Permissions.filter(id__in=permission_ids))
        return permissions
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")