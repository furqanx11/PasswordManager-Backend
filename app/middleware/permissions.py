# from fastapi import Depends, HTTPException, status
# from app.models import UserRoles, RolePermissions, Permissions
# from app.dependencies.auth import get_current_user

# async def has_permission(current_user: dict, required_permission: str):
#     if current_user['is_admin']:
#         return True
#     user_roles = await UserRoles.filter(user_id=current_user['id']).prefetch_related('role__permissions__permission')
#     for user_role in user_roles:
#         for role_permission in user_role.role.permissions:
#             if role_permission.permission.name == required_permission:
#                 return True
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="You do not have the necessary permissions",
#     )

# def permission_dependency(required_permission: str):
#     async def dependency(current_user: dict = Depends(get_current_user)):
#         await has_permission(current_user, required_permission)
#     return Depends(dependency)

from fastapi import Depends, HTTPException, status
from app.models import UserRoles, RolePermissions, Permissions
from app.dependencies.auth import get_current_user
from typing import Dict, Any

# async def has_permission(current_user: Dict[str, Any], required_permission: str) -> bool:
#     if current_user.get('is_admin'):
#         return True

#     user_roles = await UserRoles.filter(user_id=current_user['id']).prefetch_related('role__role_permissions__permission')
#     for user_role in user_roles:
#         for role_permission in user_role.role.permissions:
#             if role_permission.permission.name == required_permission:
#                 return True

#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="You do not have the necessary permissions",
#     )
async def has_permission(current_user: Dict[str, Any] , required_perm: str, user_id = None) -> bool:
    if current_user:
        user_id = current_user['id']
    else:
        user_id = user_id

    field_perms = []
    # Fetch user roles with related role details
    user_roles = await UserRoles.filter(user_id=user_id).prefetch_related('role')

    # Check if the user has the 'admin' role
    for user_role in user_roles:
        if user_role.role.name == 'admin':
            return True
        
    for user_role in user_roles:
        role_id = user_role.role.id
        # Fetch role permissions with related permission details
        role_permissions = await RolePermissions.filter(role_id=role_id).prefetch_related('permission')


        # Check if the user has the required permission
        for role_permission in role_permissions:
            if required_perm == 'FIELD:GET:MODE':
                if role_permission.permission.name.startswith('FIELD:GET:'):
                    field_perms.append(role_permission.permission.name)
            elif role_permission.permission.name == required_perm:
                return True
            
        if required_perm == 'FIELD:GET:MODE':
            return [item.split(":")[-1] for item in field_perms]

    # If no 'admin' role is found, raise an exception
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have the necessary permissions",
    )


def permission_dependency(required_permission: str):
    async def dependency(current_user: Dict[str, Any] = Depends(get_current_user)):
        await has_permission(current_user, required_permission)
    return dependency