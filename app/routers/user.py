from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models import Users, User_Pydantic
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from app.schemas.project_schema import ProjectWithFields
from app.utils.jwt import create_access_token, verify_password, get_password_hash
from datetime import timedelta
from app.dependencies.auth import get_current_user, is_admin
from app.crud.crud import CRUD
from typing import List
from app.models import UserProjects, Project_Pydantic, Projects, Field_Pydantic, Fields

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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await Users.get(username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return user_crud.get(id=current_user.id)

@router.get("/users", response_model=list[UserRead])
async def get_all_users():
    users = Users.all()
    return await User_Pydantic.from_queryset(users)


# @router.get("/users/{user_id}/projects", response_model=List[Project_Pydantic])
# async def get_user_projects(user_id: int):
#     user = await Users.get(id=user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     user_projects = await UserProjects.filter(user_id=user_id).prefetch_related('project')
#     projects = [user_project.project for user_project in user_projects]
#     return await Project_Pydantic.from_queryset(Projects.filter(id__in=[project.id for project in projects]))

@router.get("/users/{user_id}/projects", response_model=List[ProjectWithFields])
async def get_user_projects(user_id: int):
    user = await Users.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_projects = await UserProjects.filter(user_id=user_id).prefetch_related('project')
    projects = [user_project.project for user_project in user_projects]
    project_ids = [project.id for project in projects]
    
    # Fetch fields for each project
    fields = await Fields.filter(project_id__in=project_ids)
    fields_by_project = {}
    for field in fields:
        if field.project_id not in fields_by_project:
            fields_by_project[field.project_id] = []
        fields_by_project[field.project_id].append(field)
    
    # Add fields to each project
    project_data = []
    for project in projects:
        project_pydantic = await Project_Pydantic.from_tortoise_orm(project)
        project_dict = project_pydantic.dict()
        project_dict['fields'] = await Field_Pydantic.from_queryset(Fields.filter(project_id=project.id))
        project_data.append(project_dict)
    
    return project_data