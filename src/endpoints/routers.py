from fastapi import APIRouter

# import endpoints routers from v1
from src.endpoints.v1 import test_endpoint


api_router = APIRouter(prefix="")

# include routers from v1
api_router.include_router(test_endpoint.router, prefix="/api/v1/test")

