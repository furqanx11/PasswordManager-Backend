from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routers.api_routes import router
from app.exceptions.custom_exceptions import custom_validation_exception_handler
from app.exceptions import CustomValidationException
from app.config import settings

app = FastAPI()
app.add_exception_handler(CustomValidationException, custom_validation_exception_handler)
app.include_router(router)

# Tortoise ORM configuration
register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True
)

@app.get("/")
def read_root():
    return {"message": "Welcome to your Password Manager"}
