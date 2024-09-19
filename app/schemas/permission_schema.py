from app.schemas.schema import BaseSchema
from typing import Optional
from pydantic import BaseModel

class PermissionCreate(BaseModel):
    name : str
    
class PermissionUpdate(BaseModel):
    name: Optional[str] = None

class PermissionRead(BaseSchema):
    name : str

    class Config:
        orm_mode = True
