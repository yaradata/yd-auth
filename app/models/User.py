from typing import Optional

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

from passlib.hash import bcrypt
class User(Model):
    id = fields.UUIDField(pk = True)
    username = fields.CharField(100, unique = True)
    firstname = fields.CharField(100)
    lastname = fields.CharField(100)
    email = fields.CharField(80, unique = True)
    password = fields.CharField(250)
    url_profile = fields.CharField(250, null = True)
    active = fields.BooleanField(default = False)
    created_at = fields.DatetimeField(auto_now_add = True) 
    updated_at = fields.DatetimeField(auto_now = True) 
    
    @classmethod
    async def get_user(cls, username):
        return cls.get(username = username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)
    
    def __repr__(self):
        return f'<User {self.email}>'


User_Pydantic = pydantic_model_creator(User, name = 'User')
UserIn_Pydantic = pydantic_model_creator(User, name = 'UserIn', exclude_readonly = True)

def tortoise_to_pydantic(user: UserIn_Pydantic):
    user_obj = User(
        username = user.username,
        firstname = user.firstname,
        lastname = user.lastname,
        email = user.email,
        password = user.password,
        active = user.active,
        url_profile = user.url_profile
    )
    return user_obj