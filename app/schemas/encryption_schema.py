from pydantic import BaseModel

class AddKeyRequest(BaseModel):
    project_id: int
    mode_id: int
    key: str
    value: str
    description: str = None