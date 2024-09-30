from typing import Any, Dict, List, Optional, TypeVar
from tortoise.models import Model
from app.exceptions.custom_exceptions import CustomValidationException


TModel = TypeVar("TModel", bound=Model)

class CRUD:
    def __init__(self, model: TModel, model_pydantic, related_fields: Optional[List[str]] = None):
        self.model = model
        self.model_pydantic = model_pydantic
        self.related_fields = related_fields or []
    

    async def get_all(self) -> List:
        query = self.model.all()
        if self.related_fields:
            query = query.prefetch_related(*self.related_fields)
        return await query.values()

    async def create(self, item_data: Dict[str, Any]) -> TModel:
        try:
            item = await self.model.create(**item_data)
            return item
        except Exception as e:
            raise CustomValidationException(status_code=400, detail=str(e))

    async def get(self, id: str) -> Optional[Dict[str, Any]]:
        item = await self.model.filter(id=id).values()
        if not item:
            raise CustomValidationException(status_code=404, detail=f"{self.model.__name__} with id {id} does not exist.")
        
        return item[0]
    
    async def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        item = await self.model.filter(username=username).values()
        if not item:
            raise CustomValidationException(status_code=404, detail=f"{self.model.__name__} with username {username} does not exist.")
        
        return item[0]
    
    async def update(self, id: int, item_data: Dict[str, Any]) -> Optional[TModel]:
        update_data = {k: v for k, v in item_data.items() if v is not None}
        if not update_data:
            raise CustomValidationException(status_code=400, detail="No valid fields provided for update.")

        await self.model.filter(id=id).update(**update_data)

        item = await self.model.filter(id=id).first()
        if item is None:
            raise CustomValidationException(status_code=404, detail=f"{self.model.__name__} with id {id} does not exist.")
        return item

    async def delete(self, id: int) -> None:
        await self.model.filter(id=id).delete()        
        return True