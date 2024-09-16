from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models import Users, User_Pydantic
from app.schemas.user_schema import UserCreateSchema, UserReadSchema
from app.utils.jwt import create_access_token, verify_password, get_password_hash
from datetime import timedelta
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserReadSchema)
async def register_user(user: UserCreateSchema):
    user_obj = await Users.create(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        is_admin = user.is_admin
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

@router.get("/me", response_model=UserReadSchema)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user