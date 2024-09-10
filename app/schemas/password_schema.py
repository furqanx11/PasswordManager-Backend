from pydantic import BaseModel
from app.schemas.schema import BaseSchema

class PasswordCreateSchema(BaseModel):
    project_id: int
    password: str
    service: str


class PasswordReadSchema(BaseSchema):
    project_id: int
    password: str
    service: str