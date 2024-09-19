from fastapi import Depends, HTTPException,Request
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import decode_access_token
from app.models import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(request: Request = None, token: str = Depends(oauth2_scheme)):
    if not token:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Token not found in header or cookies")
    
    payload = decode_access_token(token)
    username: str = payload.get("username")
    roles: list = payload.get("roles", [])
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await Users.get(username=username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return {"username": user.username, "roles": roles, "id": user.id, "user" : user}
