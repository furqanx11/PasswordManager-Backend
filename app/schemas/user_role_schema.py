from typing import Optional
from pydantic import BaseModel
from app.schemas.schema import BaseSchema


class UserRoleCreate(BaseModel):
    user_id: int
    role_id: int

class UserRoleUpdate(BaseModel):
    user_id: Optional[int] = None
    role_id: Optional[int] = None

class UserRoleRead(BaseSchema):
    user_id: int
    role_id: int
    class Config:
        orm_mode = True