from pydantic import BaseModel
from typing import Optional

class AddKeyRequest(BaseModel):
    project_id: int
    mode_id: int
    key: str
    value: Optional[str]
    description: str = None