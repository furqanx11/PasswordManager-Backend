from app.crud.crud import CRUD
from app.schemas.field_schema import FieldCreate, FieldRead, FieldUpdate
from app.routers.routes import routes
from app.models import Fields, Field_Pydantic, Modes, Projects
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_queryset_creator
from typing import List, Optional

field = CRUD(Fields, Field_Pydantic, related_fields=['project', 'mode'])

router = routes(
    create_func=field.create,
    get_func=field.get,
    update_func=field.update,
    delete_func=field.delete,
    get_all = field.get_all,
    create_schema=FieldCreate,
    response_schema=FieldRead,
    update_schema=FieldUpdate,
    pydantic_model=Field_Pydantic,
    model_name="FIELD" 
)


additional_router = APIRouter()

@additional_router.get("/", response_model=List[FieldRead])
async def get_fields_by_mode(mode_name: Optional[str] = None, project_name: Optional[str] = None):
    project = await Projects.get_or_none(name=project_name)
    mode = await Modes.get_or_none(name=mode_name)

    if not project and not mode:
        raise HTTPException(status_code=404, detail="Not found")

    filters = {}
    if project:
        filters['project_id'] = project.id  # Use project ID in filter
    if mode:
        filters['mode_id'] = mode.id  # Use mode ID in filter

    # Using .values() to retrieve the fields directly
    fields_queryset = await Fields.filter(**filters).values('id', 'key', 'value', 'description', 'project_id', 'mode_id', 'created_at', 'updated_at')
    
    if not fields_queryset:
        raise HTTPException(status_code=404, detail="No fields found.")

    return fields_queryset

router.include_router(additional_router)
