from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.utils.encryption import load_public_key, encrypt_with_rsa
from app.models import Fields, Projects, Modes
from app.schemas.encryption_schema import AddKeyRequest
# from app.config import Tortoise

router = APIRouter()



@router.post("/add_key")
async def add_key(body: AddKeyRequest):
    public_key = load_public_key()
    encrypted_value = encrypt_with_rsa(public_key, body.value)

    project = await Projects.get_or_none(id=body.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    mode = await Modes.get_or_none(id=body.mode_id)
    if not mode:
        raise HTTPException(status_code=404, detail="Mode not found")

    field = await Fields.create(
        project=project,
        mode=mode,
        key=body.key,
        value=encrypted_value,
        description=body.description
    )

    return {"message": "Key encrypted and stored successfully!", "field_id": field.id}
