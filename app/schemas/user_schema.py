from typing import Optional, List
from pydantic import EmailStr, BaseModel, validator
from app.schemas.schema import BaseSchema
import re
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
