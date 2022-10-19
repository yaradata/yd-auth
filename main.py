from fastapi import FastAPI, Depends

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

@app.post('/token', tags=['token'])
async def token(form: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form.username + 'token'}

@app.get('/')
async def home(token: str = Depends(oauth2_scheme)):
    return RedirectResponse('/docs')

