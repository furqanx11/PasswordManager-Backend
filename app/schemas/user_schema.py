from typing import Optional, List
from pydantic import EmailStr, BaseModel, validator
from app.schemas.schema import BaseSchema
from datetime import datetime
from app.exceptions.custom_exceptions import CustomValidationException


class UserCreate(BaseModel):
    name : str
    username: str
    password: str
    email :EmailStr

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    
class UserRead(BaseSchema):
    name : str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserDetail(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectUsers(BaseModel):
    users: List[UserRead]
    project_id: int
    class Config:
        from_attributes = True