from pydantic import BaseModel
from app.schemas.schema import BaseSchema
from typing import Optional

class ProjectCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectReadSchema(BaseSchema):
    name: str
    description: Optional[str] = None