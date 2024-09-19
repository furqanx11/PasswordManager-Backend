from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class BaseModel(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

class Users(BaseModel):
    name = fields.CharField(max_length=50)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=255) 
    email = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)
    

    class PydanticMeta:
        exclude = ['password'] 

class Roles(BaseModel):
    name = fields.CharField(max_length=20)
    permissions = fields.ManyToManyField('models.Permissions', through='rolepermissions', related_name='roles')

class UserRoles(BaseModel):
    user = fields.ForeignKeyField('models.Users', related_name='roles')
    role = fields.ForeignKeyField('models.Roles', related_name='users')

class Permissions(BaseModel):
    name = fields.CharField(max_length=20)

class Projects(BaseModel):
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=255, null=True)

class UserProjects(BaseModel):
    user = fields.ForeignKeyField('models.Users', related_name='projects')
    project = fields.ForeignKeyField('models.Projects', related_name='users')

class Fields(BaseModel):
    project = fields.ForeignKeyField('models.Projects', related_name='fields')
    mode = fields.ForeignKeyField('models.Modes', related_name='fields')
    key = fields.CharField(max_length=50)
    value = fields.CharField(max_length=255)  
    description = fields.CharField(max_length=255, null=True)

class Modes(BaseModel):
    name = fields.CharField(max_length=20)

class RolePermissions(BaseModel):
    role = fields.ForeignKeyField('models.Roles', related_name='role_permissions', to_field = 'id')
    permission = fields.ForeignKeyField('models.Permissions', related_name='role_permissions', to_field = 'id')

Mode_Pydantic = pydantic_model_creator(Modes, name="Mode")
ModeIn_Pydantic = pydantic_model_creator(Modes, name="ModeIn", exclude_readonly=True)
Field_Pydantic = pydantic_model_creator(Fields, name="Field", include=("id", "key", "value", "description", "project_id", "mode_id", "created_at", "updated_at"))
FieldIn_Pydantic = pydantic_model_creator(Fields, name="FieldIn", exclude_readonly=True)
UserProject_Pydantic = pydantic_model_creator(UserProjects, name="UserProject")
UserProjectIn_Pydantic = pydantic_model_creator(UserProjects, name="UserProjectIn", exclude_readonly=True)
Project_Pydantic = pydantic_model_creator(Projects, name="Project")
ProjectIn_Pydantic = pydantic_model_creator(Projects, name="ProjectIn", exclude_readonly=True)
Permission_Pydantic = pydantic_model_creator(Permissions, name="Permission")
PermissionIn_Pydantic = pydantic_model_creator(Permissions, name="PermissionIn", exclude_readonly=True)
Role_Pydantic = pydantic_model_creator(Roles, name="Role")
RoleIn_Pydantic = pydantic_model_creator(Roles, name="RoleIn", exclude_readonly=True)
User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
RolePermission_Pydantic = pydantic_model_creator(RolePermissions, name="RolePermission")
RolePermissionIn_Pydantic = pydantic_model_creator(RolePermissions, name="RolePermissionIn", exclude_readonly=True)
UserRole_Pydantic = pydantic_model_creator(UserRoles, name="UserRole")
UserRoleIn_Pydantic = pydantic_model_creator(UserRoles, name="UserRoleIn", exclude_readonly=True)