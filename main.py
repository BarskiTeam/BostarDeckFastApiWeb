from fastapi import FastAPI

from api_v1 import users_api
from core import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users_api.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}



