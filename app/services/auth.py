import os

from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.hash import bcrypt

import jwt

from models import User
from models.User import User_Pydantic, UserIn_Pydantic, tortoise_to_pydantic

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

JWT_SECRET = os.environ.get("JWT_SECRET")


@auth_router.post('/users', response_model = User_Pydantic)
async def register_post(user: UserIn_Pydantic):
    user.password = bcrypt.hash(user.password)
    user_obj = tortoise_to_pydantic(user)
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

async def authenticate_user(username: str, password):
    user = await User.get_user(username = username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

@auth_router.post('/token')
async def token(form: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form.username, form.password)

    if not user:
        return {'error': 'invalid credentials'}

    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {'access_token': token, 'token_type': 'bearer'}