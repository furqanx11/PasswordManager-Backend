from typing import Optional
from pydantic import BaseModel
from app.schemas.schema import BaseSchema
from datetime import datetime


class FieldCreate(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    project_id: int
    mode_id: int


class FieldUpdate(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    mode_id: Optional[int] = None

class FieldRead(BaseSchema):
    id: int  # Include id field
    key: str
    value: str
    description: Optional[str] = None
    project_id: Optional[int] = None  
    mode_id: int  
    created_at: datetime 
    updated_at: datetime  


    class Config:
        from_attributes = True