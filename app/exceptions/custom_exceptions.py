from fastapi.responses import JSONResponse
from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_400_BAD_REQUEST
from pydantic import BaseModel


class CustomValidationException(Exception):
    def __init__(self, status_code: int, detail: str = ""):
        self.status_code = status_code
        self.detail = detail

async def custom_validation_exception_handler(request: Request, exc: CustomValidationException):
    if exc.detail is None:
        return Response(
            status_code=exc.status_code
        )
    if exc.status_code == 201:
        return Response(
            status_code=exc.status_code
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )