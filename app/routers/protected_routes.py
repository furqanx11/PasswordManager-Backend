from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/protected", response_model=dict)
async def read_protected_route(current_user: str = Depends(get_current_user)):
    return {"message": "This is a protected route", "user_id": current_user.username}