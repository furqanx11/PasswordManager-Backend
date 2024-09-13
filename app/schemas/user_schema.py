from typing import Optional, List
from pydantic import EmailStr, BaseModel
from app.schemas.schema import BaseSchema
from app.schemas.role_schema import RoleRead

class UserCreate(BaseModel):
    name : str
    username: str
    email: EmailStr
    password: str
    role_id: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None

class UserRead(BaseSchema):
    name : str
    username: str
    email: EmailStr
    #role_id: int

    class Config:
        orm_mode = True
