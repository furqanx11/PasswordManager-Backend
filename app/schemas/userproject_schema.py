from pydantic import BaseModel
from app.schemas.schema import BaseSchema

class UserProjectCreateSchema(BaseModel):
    user_id: int
    project_id: int

class UserProjectReadSchema(BaseSchema):
    user_id: int
    project_id: int
