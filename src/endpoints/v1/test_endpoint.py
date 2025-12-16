"""
Test endpoint
"""
from fastapi import APIRouter


router = APIRouter(tags=["Test endpoint"], redirect_slashes=True)


@router.get("/")
async def get_test() -> str:
    return "test"
