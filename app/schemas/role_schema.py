from app.schemas.schema import BaseSchema
from pydantic import BaseModel
from typing import Optional

class RoleCreate(BaseModel):
    name : str
    permissions_id : int

class RoleUpdate(BaseModel):
    name : Optional[str] = None
    permissions_id : Optional[int] = None

class RoleRead(BaseSchema):
    name : str
    permissions_id : int
    class Config:
        orm_mode = True