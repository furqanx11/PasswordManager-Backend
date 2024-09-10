from typing import Optional
from pydantic import BaseModel
from app.schemas.schema import BaseSchema

class UserCreateSchema(BaseModel):
    username: str
    password: str
    email : str
    is_admin : Optional[bool] = False           
    is_active : Optional[bool] = True


class UserReadSchema(BaseSchema):
    username: str
    email: str
    is_admin: bool
    is_active: bool

class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email : Optional[str] = None
    is_admin : Optional[bool] = None
    is_active : Optional[bool] = None
