from fastapi import FastAPI, HTTPException, APIRouter
from app.utils.encryption import load_private_key, decrypt_with_rsa
from app.models import Fields

router = APIRouter()


@router.get("/get_key/{field_id}")
async def get_key(field_id: int):
    try:
        field = await Fields.get_or_none(id=field_id)
        if not field:
            raise HTTPException(status_code=404, detail="Field not found")

        private_key = load_private_key()

        decrypted_value = decrypt_with_rsa(private_key, field.value)

        return {
            "key": field.key,
            "value": decrypted_value,
            "description": field.description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))