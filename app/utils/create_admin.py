from app.models import Users, Roles, UserRoles
from app.utils.jwt import get_password_hash

async def create_default_user():
    username = "admin"
    email = "admin@abc.com"
    name = "Admin"
    password=get_password_hash("123")

    user = await Users.get_or_none(username=username)
    if not user:
        user = await Users.create(name = name, username=username, email=email, password=password)
        return 
    else:
        return None


async def create_role():
    name = "admin"
    role = await Roles.get_or_none(name=name)
    if not role:
        role = await Roles.create(name=name)
    
async def assign_role():
    user = await Users.get(username="admin")
    role = await Roles.get(name="admin")
    
    existing_assignment = await UserRoles.filter(user_id=user.id, role_id=role.id).first()
    
    if not existing_assignment:
        await UserRoles.create(user_id=user.id, role_id=role.id)
    
async def create_admin():
    await create_default_user()
    await create_role()
    await assign_role()
    
