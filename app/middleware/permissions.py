from app.models import Roles

async def has_permission(current_user: dict, required_permission: str):
    roles = current_user.get("roles", [])
    
    for role in roles:
        user_role = await Roles.get(name=role).prefetch_related('role_permissions', 'role_permissions__permission')
        permissions = [rp.permission.allowed_api for rp in user_role.role_permissions]
        if required_permission in permissions:
            return True
    return False