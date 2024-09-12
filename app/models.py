from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Users(BaseModel):
    name = fields.CharField(max_length=50)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)
    email = fields.CharField(max_length=100, unique=True)
    role = fields.ForeignKeyField('models.Roles', related_name='users')


class Roles(BaseModel):
    name = fields.CharField(max_length=20, unique=True)


class Projects(BaseModel):
    name = fields.CharField(max_length=100, unique=True)
    description = fields.TextField(null=True)
    saved_at = fields.DatetimeField(auto_now_add=True)


class UserProject(BaseModel):
    user = fields.ForeignKeyField('models.Users', related_name='user_projects')
    project = fields.ForeignKeyField('models.Projects', related_name='project_users')


class Permissions(BaseModel):
    mode = fields.ForeignKeyField('models.Modes', related_name='permissions')
    name = fields.CharField(max_length=20, unique=True)


class RolePermissions(BaseModel):
    role = fields.ForeignKeyField('models.Roles', related_name='role_permissions')
    permission = fields.ForeignKeyField('models.Permissions', related_name='permission_roles')


class Fields(BaseModel):
    project = fields.ForeignKeyField('models.Projects', related_name='fields')
    mode = fields.ForeignKeyField('models.Modes', related_name='fields')
    key = fields.CharField(max_length=50)
    value = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255, null=True)


class Modes(BaseModel):
    name = fields.CharField(max_length=20, unique=True)


User_Pydantic = pydantic_model_creator(Users, name="User")
Project_Pydantic = pydantic_model_creator(Projects, name="Project")
UserProject_Pydantic = pydantic_model_creator(UserProject, name="UserProject")
Field_Pydantic = pydantic_model_creator(Fields, name="Field")
