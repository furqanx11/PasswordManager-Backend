from typing import Optional, List
from pydantic import EmailStr, BaseModel
from app.schemas.schema import BaseSchema
from app.schemas.role_schema import RoleRead

class UserCreate(BaseModel):
    name : str
    username: str
    email: EmailStr
    password: str

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
        orm_mode = True
