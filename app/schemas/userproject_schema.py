from typing import Optional, Union, List
from pydantic import BaseModel
from app.schemas.schema import BaseSchema


class UserProjectCreate(BaseModel):
    user_id: Union[int, List[int]]
    project_id: int

class UserProjectUpdate(BaseModel):
    user_id: Optional[List[int]] = None
    project_id: Optional[int] = None

class UserProjectRead(BaseSchema):
    user_id: int
    project_id: int
    class Config:
        from_attributes = True