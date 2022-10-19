from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.UUIDField(pk = True)
    username = fields.CharField(100)
    firstname = fields.CharField(100)
    lastname = fields.CharField(100)
    email = fields.CharField(80, unique = True)
    password = fields.CharField(250)
    url_profile = fields.CharField(250)
    active = fields.BooleanField(default = False)
    created_at = fields.DatetimeField(auto_now_add = True) 
    updated_at = fields.DatetimeField(auto_now = True) 
    
    @classmethod
    async def get_user(cls, username):
        return cls.get(username = username)

    def verify_password(self, password):
        return True

    
    def __repr__(self):
        return f'<User {self.email}>'