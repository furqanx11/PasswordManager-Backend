from fastapi import APIRouter, HTTPException, status, Depends
from typing import Type, TypeVar, Callable
from pydantic import BaseModel, ValidationError
from app.exceptions.custom_exceptions import CustomValidationException
from app.middleware.permissions import permission_dependency
from typing import List, Any, Optional
from app.models import Projects, Modes, Fields
from app.schemas.field_schema import FieldRead

TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TResponseSchema = TypeVar("TResponseSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)

def routes(
    create_func: Callable[[dict], TResponseSchema],
    get_func: Callable[[str], TResponseSchema],
    get_all : Callable[[], list[Any]],
    update_func: Callable[[str, dict], TResponseSchema],
    delete_func: Callable[[str], None],
    create_schema: Type[TCreateSchema],
    response_schema: Type[TResponseSchema],
    update_schema: Type[TUpdateSchema],
    pydantic_model: Type = None,
    model_name: str = "MODEL",
) -> APIRouter:
    router = APIRouter() 


    @router.post("/", response_model=pydantic_model, status_code=status.HTTP_201_CREATED, dependencies=[Depends(permission_dependency(f"{model_name}:CREATE"))])
    async def create(item: create_schema):
            try:
                item = await create_func(item.dict())
                if not item:
                    raise CustomValidationException(status_code=400, detail="Item not created.", pre = True)
                return item
            except ValidationError as e:
                raise CustomValidationException(status_code=400, detail=str(e))

    @router.get("/", response_model=List[FieldRead])
    async def get_fields_by_mode(mode_name: Optional[str] = None, project_name: Optional[str] = None):

        if not mode_name and not project_name:
            items = await get_all()
            return items

        project = await Projects.get_or_none(name=project_name)
        mode = await Modes.get_or_none(name=mode_name)

        if not project and not mode:
            raise HTTPException(status_code=404, detail="Not found")

        filters = {}
        if project:
            filters['project_id'] = project.id  
        if mode:
            filters['mode_id'] = mode.id  

        
        fields_queryset = await Fields.filter(**filters).values('id', 'key', 'value', 'description', 'project_id', 'mode_id', 'created_at', 'updated_at')
        
        if not fields_queryset:
            raise HTTPException(status_code=404, detail="No fields found.")

        return fields_queryset   
        
    # @router.get("/", response_model=List[response_schema], dependencies=[Depends(permission_dependency(f"{model_name}:GETALL"))])
    # async def read_all():
    #         items = await get_all()
    #         return items

    @router.get("/{id}", response_model=response_schema, dependencies=[Depends(permission_dependency(f"{model_name}:GET"))])
    async def read(id: str):
            item = await get_func(id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item

    @router.patch("/{id}", response_model=pydantic_model, dependencies=[Depends(permission_dependency(f"{model_name}:UPDATE"))])
    async def update_item(id: str, item: update_schema):
            try:
                item_data = item.dict(exclude_unset=True)
                updated_item = await update_func(id, item_data)
                if not updated_item:
                    raise HTTPException(status_code=404, detail="Item not found")
                return updated_item
            except ValidationError as e:
                raise HTTPException(status_code=422, detail=str(e))
            
    @router.delete("/{id}", response_model=dict, dependencies=[Depends(permission_dependency(f"{model_name}:DELETE"))])
    async def delete(id: str):
            item_to_delete = await get_func(id)
            if not item_to_delete:
                raise HTTPException(status_code=404, detail="Item not found")
            await delete_func(id)
            return {"detail": "Item deleted successfully"}

    return router

