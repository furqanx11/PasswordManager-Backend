from app.models import Users
from app.utils.jwt import get_password_hash
async def create_default_user():
    username = "admin"
    email = "admin@abc.com"
    name = "Admin"
    password=get_password_hash("123")

    user = await Users.get_or_none(username=username)
    if not user:
        user = await Users.create(name = name, username=username, email=email, password=password)