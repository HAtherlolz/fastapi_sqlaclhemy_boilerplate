from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import User
from src.repositories.users import UserRepository
from src.schemas.users import UserCreateRequestSchema, UserJwtSchema
from src.utils.jwt import JWTService
from src.utils.password_hashing import hash_password, verify_password


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def create_user(self, user_data: UserCreateRequestSchema) -> dict[str, str]:
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User already exists")

        first_name, last_name = user_data.full_name.split()

        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            first_name=first_name,
            last_name=last_name,
        )

        user = await self.user_repo.create(user)

        access_token = JWTService.create_access_token(user.id)
        refresh_token = JWTService.create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}

    async def get_user_by_token(self, token: str) -> User:
        payload = JWTService.decode_token(token)

        if payload.get("type") != "access":
            raise ValueError("Invalid token type")

        user_id = int(payload["sub"])
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        return user

    async def refresh_tokens(self, refresh_token: str) -> dict[str, str]:
        payload = JWTService.decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = int(payload["sub"])
        user = await self.user_repo.get_by_id(user_id)

        if not user or not user.is_active:
            raise ValueError("User not found or inactive")

        new_access = JWTService.create_access_token(user.id)
        new_refresh = JWTService.create_refresh_token(user.id)

        return {"access_token": new_access, "refresh_token": new_refresh}

    async def login(self, email: str, password: str) -> UserJwtSchema:
        user = await self.user_repo.get_by_email(email)

        if not user or not user.is_active:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        return UserJwtSchema(
            access_token=JWTService.create_access_token(user.id),
            refresh_token=JWTService.create_refresh_token(user.id),
        )
