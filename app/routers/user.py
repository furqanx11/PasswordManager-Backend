from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import Users, User_Pydantic
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from app.schemas.project_schema import ProjectWithFields
from app.utils.jwt import create_access_token, verify_password, get_password_hash
from datetime import timedelta
from app.dependencies.auth import get_current_user
from app.crud.crud import CRUD
from typing import List
from app.models import UserProjects, Project_Pydantic,Field_Pydantic, Fields
from app.middleware.permissions import permission_dependency

router = APIRouter()
user_crud = CRUD(Users, User_Pydantic)

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate):
    user_obj = await Users.create(
        name = user.name,
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )
    return await User_Pydantic.from_tortoise_orm(user_obj)

@router.post("/login")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await Users.get_or_none(username=form_data.username)  
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = await create_access_token(user, expires_delta=access_token_expires)  
    
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=1800)
    return {"access_token": access_token, "token_type": "bearer"}

@router.patch("/me", response_model=UserRead)
async def update_user_me(user_update: UserUpdate, current_user: Users = Depends(get_current_user)):
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(current_user['user'], key, value)
    await current_user.save()
    return await User_Pydantic.from_tortoise_orm(current_user)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(current_user: Users = Depends(get_current_user)):
    await current_user.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    print(current_user)
    print(current_user['username'])
    return await user_crud.get_by_username(username=current_user["username"])

@router.get("/users", response_model=list[UserRead], dependencies=[Depends(permission_dependency("USER:LIST"))])
async def get_all_users():
    users = Users.all()
    return await User_Pydantic.from_queryset(users)

# @router.get("/user/{user_id}/projects", response_model=List[ProjectWithFields], dependencies=[Depends(permission_dependency("USER:PROJECTS"))])
# async def get_user_projects(user_id: int):
#     user = await Users.get(id=user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     user_projects = await UserProjects.filter(user_id=user_id).prefetch_related('project')
#     projects = [user_project.project for user_project in user_projects]
#     project_ids = [project.id for project in projects]
    
#     fields = await Fields.filter(project_id__in=project_ids).prefetch_related('project', 'mode')
#     fields_by_project = {}
#     for field in fields:
#         if field.project_id not in fields_by_project:
#             fields_by_project[field.project_id] = []
#         fields_by_project[field.project_id].append(field)
    
#     project_data = []
#     for project in projects:
#         project_pydantic = await Project_Pydantic.from_tortoise_orm(project)
#         project_dict = project_pydantic.dict()
#         project_dict['fields'] = await Field_Pydantic.from_queryset(Fields.filter(project_id=project.id))
#         project_data.append(project_dict)
    
#     return project_data

@router.get("/user/{user_id}/projects", response_model=List[ProjectWithFields])
async def get_user_projects(user_id: int):
    user = await Users.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_projects = await UserProjects.filter(user_id=user_id).prefetch_related('project')
    projects = [user_project.project for user_project in user_projects]
    project_ids = [project.id for project in projects]

    # Ensure that fields include project_id and mode_id
    fields = await Fields.filter(project_id__in=project_ids).prefetch_related('project', 'mode')
    
    fields_by_project = {}
    for field in fields:
        if field.project_id not in fields_by_project:
            fields_by_project[field.project_id] = []
        fields_by_project[field.project_id].append(field)

    project_data = []
    for project in projects:
        project_pydantic = await Project_Pydantic.from_tortoise_orm(project)
        project_dict = project_pydantic.dict()

        # Use Field_Pydantic to serialize the fields properly, ensuring project_id and mode_id are included
        project_dict['fields'] = await Field_Pydantic.from_queryset(
            Fields.filter(project_id=project.id).prefetch_related('project', 'mode')
        )
        project_data.append(project_dict)

    return project_data


@router.get("/user/{user_id}", response_model=UserRead, dependencies=[Depends(permission_dependency("USER:GET"))])
async def get_user_by_id(user_id: int):
    user = await Users.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await User_Pydantic.from_tortoise_orm(user)

@router.patch("/user/{user_id}", response_model=UserRead, dependencies=[Depends(permission_dependency("USER:UPDATE"))])
async def update_user_by_id(user_id: int, user_update: UserUpdate):
    user = await Users.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    await user.save()
    return await User_Pydantic.from_tortoise_orm(user)

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(permission_dependency("USER:DELETE"))])
async def delete_user_by_id(user_id: int):
    user = await Users.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)