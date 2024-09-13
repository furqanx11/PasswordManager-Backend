from app.schemas.schema import BaseSchema
from pydantic import BaseModel
from typing import Optional

class RoleCreate(BaseModel):
    name : str

class RoleUpdate(BaseModel):
    name : Optional[str] = None

class RoleRead(BaseSchema):
    name : str
    class Config:
        orm_mode = True