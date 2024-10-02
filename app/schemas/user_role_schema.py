from typing import Optional, Union, List
from pydantic import BaseModel
from app.schemas.schema import BaseSchema


class UserRoleCreate(BaseModel):
    user_id: int
    role_id: Union[int, List[int]]

class UserRoleUpdate(BaseModel):
    user_id: Optional[int] = None
    role_id: Optional[List[int]] = None

class UserRoleRead(BaseSchema):
    user_id: int
    role_id: int
    class Config:
        from_attributes = True