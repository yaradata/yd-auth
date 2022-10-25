import uvicorn, os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from databases.database import init_database
from services import auth

APP_PORT = os.getenv('APP_PORT')
APP_RELOAD = os.getenv('APP_RELOAD')
APP_WORKERS = os.getenv('APP_WORKERS')

app = FastAPI()

@app.get('/')
async def home():
    return RedirectResponse('/docs')


init_database(app)
app.include_router(auth.auth_router, tags = ['auth'])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(APP_PORT), reload=APP_RELOAD, workers=int(APP_WORKERS)) 