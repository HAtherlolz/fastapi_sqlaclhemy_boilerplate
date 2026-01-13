from fastapi import APIRouter

from src.endpoints.v1 import users


api_router = APIRouter(prefix="/api/v1")

# include routers from v1
api_router.include_router(users.router, prefix="/users")
