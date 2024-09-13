from app.schemas.schema import BaseSchema
from typing import Optional
from pydantic import BaseModel

class ModeCreate(BaseModel):
    name : str

class ModeUpdate(BaseModel):
    name : Optional[str] = None

class ModeRead(BaseSchema):
    name : str
    class Config:
        orm_mode = True
