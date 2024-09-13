from app.crud.crud import CRUD
from app.schemas.field_schema import FieldCreate, FieldRead, FieldUpdate
from app.routers.routes import routes
from app.models import Field, Field_Pydantic

field = CRUD(Field, Field_Pydantic)

router = routes(
    create_func=field.create,
    get_func=field.get,
    update_func=field.update,
    delete_func=field.delete,
    create_schema=FieldCreate,
    response_schema=FieldRead,
    update_schema=FieldUpdate
)