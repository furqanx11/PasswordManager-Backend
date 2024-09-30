from typing import Optional, List
from pydantic import EmailStr, BaseModel, validator
from app.schemas.schema import BaseSchema
import re


class UserCreate(BaseModel):
    name : str
    username: str
    password: str
    @validator('email')
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email address')
        return v


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
