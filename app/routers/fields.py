# from app.crud.crud import CRUD
# from app.schemas.field_schema import FieldCreate, FieldRead, FieldUpdate
# from app.routers.routes import routes
# from app.models import Fields, Field_Pydantic, Modes, Projects
# from fastapi import APIRouter, HTTPException
# from typing import List, Optional
# from fastapi import HTTPException, APIRouter
# from app.utils.encryption import load_public_key, encrypt_with_rsa
# from app.models import Fields, Projects, Modes
# from app.schemas.encryption_schema import AddKeyRequest
# from app.utils.encryption import load_private_key, decrypt_with_rsa

# field = CRUD(Fields, Field_Pydantic, related_fields=['project', 'mode'])

# # router = routes(
# #     create_func=field.create,
# #     get_func=field.get,
# #     update_func=field.update,
# #     delete_func=field.delete,
# #     get_all = field.get_all,
# #     create_schema=FieldCreate,
# #     response_schema=FieldRead,
# #     update_schema=FieldUpdate,
# #     pydantic_model=Field_Pydantic,
# #     model_name="FIELD" 
# # )


# router = APIRouter()

# @router.post("/add_key")
# async def add_key(body: AddKeyRequest):
#     public_key = load_public_key()
#     encrypted_value = encrypt_with_rsa(public_key, body.value)

#     project = await Projects.get_or_none(id=body.project_id)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")

#     mode = await Modes.get_or_none(id=body.mode_id)
#     if not mode:
#         raise HTTPException(status_code=404, detail="Mode not found")

#     field = await Fields.create(
#         project=project,
#         mode=mode,
#         key=body.key,
#         value=encrypted_value,
#         description=body.description
#     )

#     return {"message": "Key encrypted and stored successfully!", "field_id": field.id}

# @router.get("/get_key/{field_id}")
# async def get_key(field_id: int):
#     try:
#         field = await Fields.get_or_none(id=field_id)
#         if not field:
#             raise HTTPException(status_code=404, detail="Field not found")

#         private_key = load_private_key()

#         decrypted_value = decrypt_with_rsa(private_key, field.value)

#         return {
#             "key": field.key,
#             "value": decrypted_value,
#             "description": field.description
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.delete("/delete_key/{field_id}")
# async def delete_key(field_id: int):
#     field = await Fields.get_or_none(id=field_id)
#     if not field:
#         raise HTTPException(status_code=404, detail="Field not found")

#     await field.delete()
#     return {"message": "Key deleted successfully"}

# @router.patch("/update_key/{field_id}")
# async def update_key(field_id: int, body: AddKeyRequest):
#     field = await Fields.get_or_none(id=field_id)
#     if not field:
#         raise HTTPException(status_code=404, detail="Field not found")

#     if body.value:
#         public_key = load_public_key()
#         encrypted_value = encrypt_with_rsa(public_key, body.value)
#     else:
#         encrypted_value = field.value  # Keep current value

#     field.key = body.key if body.key else field.key
#     field.value = encrypted_value
#     field.description = body.description if body.description else field.description

#     await field.save()

#     return {"message": "Key updated successfully", "field_id": field.id}




# router.get("/", response_model=List[FieldRead])
# async def get_fields_by_mode(mode_name: Optional[str] = None, project_name: Optional[str] = None):
#     project = await Projects.get_or_none(name=project_name)
#     mode = await Modes.get_or_none(name=mode_name)

#     if not project and not mode:
#         raise HTTPException(status_code=404, detail="Not found")

#     filters = {}
#     if project:
#         filters['project_id'] = project.id  # Use project ID in filter
#     if mode:
#         filters['mode_id'] = mode.id  # Use mode ID in filter

#     # Using .values() to retrieve the fields directly
#     fields_queryset = await Fields.filter(**filters).values('id', 'key', 'value', 'description', 'project_id', 'mode_id', 'created_at', 'updated_at')
    
#     if not fields_queryset:
#         raise HTTPException(status_code=404, detail="No fields found.")

#     return fields_queryset

# # router.include_router(additional_router)


from app.crud.crud import CRUD
from app.schemas.field_schema import FieldCreate, FieldRead, FieldUpdate
from app.routers.routes import routes
from app.models import Fields, Field_Pydantic, Modes, Projects
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.utils.encryption import load_public_key, encrypt_with_rsa, load_private_key, decrypt_with_rsa
from app.schemas.encryption_schema import AddKeyRequest
from app.middleware.permissions import permission_dependency

field = CRUD(Fields, Field_Pydantic, related_fields=['project', 'mode'])

router = APIRouter()

from fastapi import Depends, status

@router.post("/add_key", status_code=status.HTTP_201_CREATED, dependencies=[Depends(permission_dependency("field:CREATE"))])
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

@router.get("/get_key/{field_id}", dependencies=[Depends(permission_dependency("field:GET"))])
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

@router.delete("/delete_key/{field_id}", dependencies=[Depends(permission_dependency("field:DELETE"))])
async def delete_key(field_id: int):
    field = await Fields.get_or_none(id=field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    await field.delete()
    return {"message": "Key deleted successfully"}

@router.patch("/update_key/{field_id}", dependencies=[Depends(permission_dependency("field:UPDATE"))])
async def update_key(field_id: int, body: AddKeyRequest):
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

@router.get("/", response_model=List[FieldRead], dependencies=[Depends(permission_dependency(f"field:GETALL"))])
async def get_fields_by_mode(mode_name: Optional[str] = None, project_name: Optional[str] = None):
    if not project_name and not mode_name:
        fields_queryset = await Fields.all().values(
            'id', 'key', 'value', 'description', 'project_id', 'mode_id', 'created_at', 'updated_at'
        )
        return fields_queryset

    project = await Projects.get_or_none(name=project_name)
    mode = await Modes.get_or_none(name=mode_name)

    if not project and not mode:
        raise HTTPException(status_code=404, detail="Project or Mode not found")

    filters = {}
    if project:
        filters['project_id'] = project.id 
    if mode:
        filters['mode_id'] = mode.id  

    # Retrieve the filtered results
    fields_queryset = await Fields.filter(**filters).values(
        'id', 'key', 'value', 'description', 'project_id', 'mode_id', 'created_at', 'updated_at'
    )
    
    if not fields_queryset:
        raise HTTPException(status_code=404, detail="No fields found.")

    return fields_queryset

@router.get("/fields", response_model=List[FieldRead])
async def get_all_fields():
    return await field.get_all()