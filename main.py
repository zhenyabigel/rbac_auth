from fastapi import FastAPI
from const import API_DESCRIPTION, API_TITLE, __version__
from routers.auth import auth_router

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=__version__)

app.include_router(auth_router)

