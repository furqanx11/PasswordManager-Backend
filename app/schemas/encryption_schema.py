from pydantic import BaseModel
from typing import Optional

class AddKeyRequest(BaseModel):
    project_id: int
    mode_id: int
    key: str
    value: Optional[str]
    description: str = None

class update_key(BaseModel):
    project_id: Optional[int] = None
    mode_id: Optional[int] = None
    key: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None