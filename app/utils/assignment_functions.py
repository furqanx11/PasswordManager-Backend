from app.models import UserProjects, RolePermissions
from app.schemas.userproject_schema import UserProjectCreate
from app.schemas.role_permission_schema import RolePermissionCreate
from fastapi import HTTPException, status

async def assign_project_to_users(project_assignment_data: UserProjectCreate):
    try:
        for user_id in project_assignment_data.user_id:
            await UserProjects.create(user_id=user_id, project_id=project_assignment_data.project_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def assign_permissions(permission_assignment_data: RolePermissionCreate):
    try:
        for permission_id in permission_assignment_data.permission_id:
            await RolePermissions.create(role_id=permission_assignment_data.role_id, permission_id=permission_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))