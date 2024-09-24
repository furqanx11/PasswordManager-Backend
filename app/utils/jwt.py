import jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from fastapi import HTTPException
from app.models import Users, UserRoles

SECRET_KEY = "abcd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 99999999999999999

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_access_token(user: Users, expires_delta: Optional[timedelta] = None):
    user_roles = await UserRoles.filter(user=user.id).select_related('role')
    role_names = [user_role.role.name for user_role in user_roles]

    to_encode = {"sub": user.username, "roles": role_names}
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: list = payload.get("roles", [])  # Extract roles from token
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "roles": roles}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
