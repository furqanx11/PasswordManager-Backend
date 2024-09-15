from fastapi import APIRouter, HTTPException, status, Depends
from typing import Type, TypeVar, Callable
from pydantic import BaseModel, ValidationError
from app.exceptions.custom_exceptions import CustomValidationException
from app.dependencies.auth import get_current_user
from app.middleware.permissions import has_permission

TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TResponseSchema = TypeVar("TResponseSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)

def routes(
    create_func: Callable[[dict], TResponseSchema],
    get_func: Callable[[str], TResponseSchema],
    update_func: Callable[[str, dict], TResponseSchema],
    delete_func: Callable[[str], None],
    create_schema: Type[TCreateSchema],
    response_schema: Type[TResponseSchema],
    update_schema: Type[TUpdateSchema],
    pydantic_model: Type = None
) -> APIRouter:
    router = APIRouter() 


    @router.post("/", response_model=pydantic_model, status_code=status.HTTP_201_CREATED)
    async def create(item: create_schema, current_user: dict = Depends(get_current_user)):
            if not await has_permission(current_user, "create"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to create"
                )
            try:
                item = await create_func(item.dict())
                if not item:
                    raise CustomValidationException(status_code=400, detail="Item not created.", pre = True)
                return item
            except ValidationError as e:
                raise CustomValidationException(status_code=400, detail=str(e))

    @router.get("/{id}", response_model=pydantic_model)
    async def read(id: str):
            item = await get_func(id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item

    @router.patch("/{id}", response_model=pydantic_model)
    async def update_item(id: str, item: update_schema):
            try:
                item_data = item.dict(exclude_unset=True)
                updated_item = await update_func(id, item_data)
                if not updated_item:
                    raise HTTPException(status_code=404, detail="Item not found")
                return updated_item
            except ValidationError as e:
                raise HTTPException(status_code=422, detail=str(e))
            
    @router.delete("/{id}", response_model=dict)
    async def delete(id: str):
            item_to_delete = await get_func(id)
            if not item_to_delete:
                raise HTTPException(status_code=404, detail="Item not found")
            await delete_func(id)
            return {"detail": "Item deleted successfully"}

    return router

