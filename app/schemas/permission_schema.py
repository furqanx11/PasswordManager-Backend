from app.schemas.schema import BaseSchema
from typing import Optional, List
from pydantic import BaseModel

class PermissionCreate(BaseModel):
    name : str
    
class PermissionUpdate(BaseModel):
    name: Optional[str] = None

class PermissionRead(BaseSchema):
    name : str

    class Config:
        from_attributes = True

class RolePermissionResponse(BaseModel):
    role_id: int
    permissions: List[PermissionRead]

    class config:
        from_attributes = True