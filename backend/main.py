from fastapi import FastAPI

from backend.api import api_router
from backend.db import get_database

app = FastAPI(debug=True)


@app.on_event("startup")
async def startup():
    await get_database().connect()


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()

app.include_router(api_router)


# from fastapi import FastAPI
# app = FastAPI()
# @app.get("/")
# def home():
#     return {"Hello": "FastAPI"}