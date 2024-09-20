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
    project_id: Optional[int] = None  # Include project_id field
    mode_id: int  # Include mode_id field
    created_at: datetime  # Include created_at field
    updated_at: datetime  # Include updated_at field


    class Config:
        orm_mode = True