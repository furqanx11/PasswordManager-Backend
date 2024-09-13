from pydantic import BaseModel
from app.schemas.schema import BaseSchema
from typing import Optional, List


class ProjectCreate(BaseModel):
    name : str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectRead(BaseSchema):
    name : str
    description: Optional[str] = None
    class Config:
        orm_mode = True
