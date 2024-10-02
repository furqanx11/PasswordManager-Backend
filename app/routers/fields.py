from app.crud.crud import CRUD
from app.schemas.field_schema import FieldRead
from app.models import Fields, Field_Pydantic, Modes, Projects
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from app.utils.encryption import load_public_key, encrypt_with_rsa, load_private_key, decrypt_with_rsa
from app.schemas.encryption_schema import AddKeyRequest, update_key
from app.middleware.permissions import permission_dependency

field = CRUD(Fields, Field_Pydantic, related_fields=['project', 'mode'])

router = APIRouter()


@router.post("/add_key", status_code=status.HTTP_201_CREATED, dependencies=[Depends(permission_dependency("FIELD:CREATE"))])
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
        project_id=body.project_id,
        mode_id=body.mode_id,
        key=body.key,
        value=encrypted_value,
        description=body.description
    )

    return {"message": "Key encrypted and stored successfully!", "field_id": field.id}

@router.get("/get_key/{field_id}", dependencies=[Depends(permission_dependency("FIELD:GET"))])
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

@router.delete("/delete_key/{field_id}", dependencies=[Depends(permission_dependency("FIELD:DELETE"))])
async def delete_key(field_id: int):
    field = await Fields.get_or_none(id=field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    await field.delete()
    return {"message": "Key deleted successfully"}

@router.patch("/update_key/{field_id}", dependencies=[Depends(permission_dependency("FIELD:UPDATE"))])
async def update_key(field_id: int, body: update_key):
    field = await Fields.get_or_none(id=field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    if body.value:
        public_key = load_public_key()
        encrypted_value = encrypt_with_rsa(public_key, body.value)
    else:
        encrypted_value = field.value  # Keep current value

    field.key = body.key if body.key else field.key
    field.value = encrypted_value
    field.description = body.description if body.description else field.description

    await field.save()

    return {"message": "Key updated successfully", "field_id": field.id}

    
async def get_fields_by_mode(
    mode_names: Optional[List[str]] = Query(None, alias="mode_name"),
    project_name: Optional[str] = None
):
    if not project_name:
        raise HTTPException(status_code=400, detail="Project name must be provided")

    project = await Projects.get_or_none(name=project_name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    filters = {'project_id': project.id}

    if mode_names:
        modes = await Modes.filter(name__in=mode_names).values('id', 'name')
        if not modes:
            raise HTTPException(status_code=404, detail="Modes not found")
        mode_ids = [mode['id'] for mode in modes]
        filters['mode_id__in'] = mode_ids

    fields_queryset = await Fields.filter(**filters).values(
        'id', 'key', 'value', 'description', 'project_id', 'mode_id', 'created_at', 'updated_at'
    )
    
    if not fields_queryset:
        raise HTTPException(status_code=404, detail="No fields found.")
    
    private_key = load_private_key()
    for field in fields_queryset:
        decrypted_value = decrypt_with_rsa(private_key, field['value'])
        field['value'] = decrypted_value

    return fields_queryset