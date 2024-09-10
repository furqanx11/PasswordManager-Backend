from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)
    email = fields.CharField(max_length=100, unique=True)
    is_active = fields.BooleanField(default=True)
    is_admin = fields.BooleanField(default=False)


class Project(BaseModel):
    name = fields.CharField(max_length=100, unique=True)
    description = fields.TextField(null=True)


class UserProject(BaseModel):
    user = fields.ForeignKeyField('models.User', related_name='projects')
    project = fields.ForeignKeyField('models.Project', related_name='users')


class Password(BaseModel):
    project = fields.ForeignKeyField('models.Project', related_name='passwords')
    password = fields.CharField(max_length=256)
    service = fields.CharField(max_length=100)



User_Pydantic = pydantic_model_creator(User, name="User")
Project_Pydantic = pydantic_model_creator(Project, name="Project")
UserProject_Pydantic = pydantic_model_creator(UserProject, name="UserProject")
Password_Pydantic = pydantic_model_creator(Password, name="Password")