import os
from urllib import response

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.responses import RedirectResponse, Response

from passlib.hash import bcrypt

import jwt

from models.User import User_Pydantic, UserIn_Pydantic, pydantic_to_tortoise, User

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

JWT_SECRET = os.environ.get("JWT_SECRET")


@auth_router.post('/register', response_model = User_Pydantic)
async def register_post(user: UserIn_Pydantic):
    if await User.get_or_none(username = user.username) is not None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Username already exists"
        )

    if await User.get_or_none(email = user.email) is not None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "User already exists"
        )
    
    user.password = bcrypt.hash(user.password)
    user_obj = pydantic_to_tortoise(user)
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

async def authenticate_user(username: str, password):
    user = await User.get(username = username)
   
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
    
    #concert some data into str for json serialization
    user_obj.id = str(user_obj.id)
    user_obj.created_at = str(user_obj.created_at)
    user_obj.updated_at = str(user_obj.updated_at)


    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {'access_token': token, 'token_type': 'bearer'}

@auth_router.get('/users/me', response_model = User_Pydantic)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id = payload.get('id'))
    except:
        raise HTTPException (
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid credential'
        )

    return await User_Pydantic.from_tortoise_orm(user)

@auth_router.get('/logout')
async def logout(token: str = Depends(oauth2_scheme)):
    print(token)
    return RedirectResponse('/docs').delete_cookie(token)