from app.crud.crud import CRUD
from app.schemas.mode_schema import ModeCreate, ModeRead, ModeUpdate
from app.routers.routes import routes
from app.models import Modes, Mode_Pydantic

mode = CRUD(Modes, Mode_Pydantic)

router = routes(
    create_func=mode.create,
    get_func=mode.get,
    update_func=mode.update,
    delete_func=mode.delete,
    get_all = mode.get_all,
    create_schema=ModeCreate,
    response_schema=ModeRead,
    update_schema=ModeUpdate,
    pydantic_model= Mode_Pydantic
)