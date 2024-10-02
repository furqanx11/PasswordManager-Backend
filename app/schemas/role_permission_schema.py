from app.schemas.schema import BaseSchema
from typing import Optional, Union, List
from pydantic import BaseModel, Field
from app.models import Permissions

class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: Union[int, List[int]]
class RolePermissionUpdate(BaseModel):
    role_id : Optional[int] = None
    permission_id : Optional[List[int]] = None

class RolePermissionRead(BaseSchema):
    role_id: int
    permission_id: int
    class Config:
        from_attributes = True
