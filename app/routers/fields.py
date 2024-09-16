from app.crud.crud import CRUD
from app.schemas.field_schema import FieldCreate, FieldRead, FieldUpdate
from app.routers.routes import routes
from app.models import Fields, Field_Pydantic, Modes, Projects
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_queryset_creator
from typing import List, Optional

field = CRUD(Fields, Field_Pydantic)

router = routes(
    create_func=field.create,
    get_func=field.get,
    update_func=field.update,
    delete_func=field.delete,
    get_all = field.get_all,
    create_schema=FieldCreate,
    response_schema=FieldRead,
    update_schema=FieldUpdate,
    pydantic_model=Field_Pydantic
)


additional_router = APIRouter()

@additional_router.get("/", response_model=List[Field_Pydantic])
async def get_fields_by_mode(mode_name: Optional[str] = None, project_name: Optional[str] = None):
    project = await Projects.get_or_none(name=project_name)
    mode = await Modes.get_or_none(name=mode_name)

    if not project and not mode:
        raise HTTPException(status_code=404, detail="Not found")

    filters = {}
    if project:
        filters['project'] = project
    if mode:
        filters['mode'] = mode

    fields_queryset = Fields.filter(**filters)
    fields = await Field_Pydantic.from_queryset(fields_queryset)
    return fields

router.include_router(additional_router)