from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routers.api_routes import router
from app.exceptions.custom_exceptions import custom_validation_exception_handler
from app.exceptions import CustomValidationException
from app.db import init
from app.utils.create_admin import create_admin

app = FastAPI()
app.add_exception_handler(CustomValidationException, custom_validation_exception_handler)
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await init()
    await create_admin()

@app.get("/get_all", tags=["OpenAPI"])
async def get_openapi_schema():
    openapi_schema = app.openapi()
    filtered_paths = {
        path: {
            method: {
                "summary": details.get("summary", "")
            }
            for method, details in methods.items()
        }
        for path, methods in openapi_schema["paths"].items()
    }
    return {"paths": filtered_paths}
