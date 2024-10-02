from pydantic import BaseModel
from app.schemas.schema import BaseSchema
from typing import Optional, List
from app.models import Field_Pydantic
from app.schemas.field_schema import FieldRead

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
        from_attributes = True

class ProjectWithFields(BaseSchema):
    name: str
    description: Optional[str] = None
    fields: Optional[List[FieldRead]] = None