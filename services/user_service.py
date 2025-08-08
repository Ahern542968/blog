from datetime import datetime, timedelta

from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.user import User
from schemas.user import Token
from configs.configs import settings
from utils.exceptions import FlictException, NotFoundException, UnauthorizedException, ForbiddenException
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    def get_hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_access_token(username):
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": username, "exp": expire}
        access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return access_token

    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> User:
        result = await session.exec(select(User).where(User.username == username))
        return result.first()

    @staticmethod
    async def create_user(session: AsyncSession, username: str, password: str) -> User:
        user = await UserService.get_user_by_username(session, username)
        if user: raise FlictException()

        hash_password = UserService.get_hash_password(password)
        new_user = User(username=username, hash_password=hash_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

    @staticmethod
    async def get_users(session: AsyncSession, skip: int = 0, limit: int = 100):
        statement = select(User).offset(skip).limit(limit)
        results = await session.exec(statement)
        return results.all()

    @staticmethod
    async def login(session, username, password):
        user = await UserService.get_user_by_username(session, username)
        if not user: raise NotFoundException()

        is_valid = UserService.verify_password(password, user.hash_password)
        if not is_valid: raise UnauthorizedException()

        access_token = UserService.get_access_token(user.username)
        return Token(access_token=access_token, token_type=settings.ACCESS_TOKEN_TYPE)

    @staticmethod
    async def update_password(session: AsyncSession, username: str, old_password: str, new_password: str) -> User:
        user = await UserService.get_user_by_username(session, username)
        if not user: raise NotFoundException()

        if not UserService.verify_password(old_password, user.hash_password): raise ForbiddenException()

        user.hash_password = UserService.get_hash_password(new_password)
        session.add(user)
        await session.commit()
        return user
