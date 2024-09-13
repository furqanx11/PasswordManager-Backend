from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class BaseModel(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel):
    role = fields.ForeignKeyField('models.Role', related_name='users')
    name = fields.CharField(max_length=50)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=255) 
    email = fields.CharField(max_length=255, unique=True)

    class PydanticMeta:
        exclude = ['password'] 


class Role(BaseModel):
    name = fields.CharField(max_length=20)

class Permission(BaseModel):
    name = fields.CharField(max_length=20)
    allowed_api = fields.CharField(max_length=50)

class Project(BaseModel):
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=255, null=True)

class UserProject(BaseModel):
    user = fields.ForeignKeyField('models.User', related_name='projects')
    project = fields.ForeignKeyField('models.Project', related_name='users')


class Field(BaseModel):
    project = fields.ForeignKeyField('models.Project', related_name='fields')
    mode = fields.ForeignKeyField('models.Mode', related_name='fields')
    key = fields.CharField(max_length=50)
    value = fields.CharField(max_length=255)  
    description = fields.CharField(max_length=255, null=True)


class Mode(BaseModel):
    name = fields.CharField(max_length=20)

class RolePermission(BaseModel):
    role = fields.ForeignKeyField('models.Role', related_name='role_permissions')
    permission = fields.ForeignKeyField('models.Permission', related_name='role_permissions')

Mode_Pydantic = pydantic_model_creator(Mode, name="Mode")
ModeIn_Pydantic = pydantic_model_creator(Mode, name="ModeIn", exclude_readonly=True)
Field_Pydantic = pydantic_model_creator(Field, name="Field")
FieldIn_Pydantic = pydantic_model_creator(Field, name="FieldIn", exclude_readonly=True)
UserProject_Pydantic = pydantic_model_creator(UserProject, name="UserProject")
UserProjectIn_Pydantic = pydantic_model_creator(UserProject, name="UserProjectIn", exclude_readonly=True)
Project_Pydantic = pydantic_model_creator(Project, name="Project")
ProjectIn_Pydantic = pydantic_model_creator(Project, name="ProjectIn", exclude_readonly=True)
Permission_Pydantic = pydantic_model_creator(Permission, name="Permission")
PermissionIn_Pydantic = pydantic_model_creator(Permission, name="PermissionIn", exclude_readonly=True)
Role_Pydantic = pydantic_model_creator(Role, name="Role")
RoleIn_Pydantic = pydantic_model_creator(Role, name="RoleIn", exclude_readonly=True)
User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
RolePermission_Pydantic = pydantic_model_creator(RolePermission, name="RolePermission")
RolePermissionIn_Pydantic = pydantic_model_creator(RolePermission, name="RolePermissionIn", exclude_readonly=True)