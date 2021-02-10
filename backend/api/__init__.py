from fastapi import APIRouter

from backend.api.datasets import datasets_router
from backend.api.users import users_router
from backend.api.users2 import users2_router

api_router = APIRouter()

api_router.include_router(datasets_router)
api_router.include_router(users_router)
api_router.include_router(users2_router)
