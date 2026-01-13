"""
Test endpoint
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel.ext.asyncio.session import AsyncSession

from src.dependecies.db_session import get_session
from src.dependecies.jwt import get_current_user
from src.models import User
from src.schemas.users import UserCreateRequestSchema, UserJwtSchema, UserDetailSchema, UserLoginRequestSchema, \
    RefreshTokenRequestSchema
from src.services.users import UserService

router = APIRouter(tags=["Users"], redirect_slashes=True)


@router.post("", response_model=UserJwtSchema)
async def create_user(
        user: UserCreateRequestSchema,
        session: AsyncSession = Depends(get_session)
):
    user_service = UserService(session)
    try:
        tokens = await user_service.create_user(user_data=user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return tokens


@router.get(
    "/me",
    response_model=UserDetailSchema,
)
async def get_me(
    user: User = Depends(get_current_user),
):
    return user


@router.post(
    "/login",
    response_model=UserJwtSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: UserLoginRequestSchema,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)

    try:
        return await service.login(
            email=data.email,
            password=data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/refresh",
    response_model=UserJwtSchema,
    status_code=status.HTTP_200_OK,
)
async def refresh_tokens(
    data: RefreshTokenRequestSchema,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)

    try:
        return await service.refresh_tokens(data.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
