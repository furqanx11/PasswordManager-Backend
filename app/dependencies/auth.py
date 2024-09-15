from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import decode_access_token
from app.models import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username: str = payload.get("username")
    roles: list = payload.get("roles", [])
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await Users.get(username=username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return {"username": user.username, "roles": roles}

async def is_admin(current_user: Users = Depends(get_current_user)):
    if current_user.is_admin == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the necessary permissions",
        )
    return current_user