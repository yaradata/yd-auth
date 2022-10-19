from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from databases.database import init_database
from services import auth

app = FastAPI()

@app.get('/')
async def home():
    return RedirectResponse('/docs')


init_database(app)
app.include_router(auth.auth_router, tags = ['auth'])