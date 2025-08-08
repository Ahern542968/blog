from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError
from sqlmodel.ext.asyncio.session import AsyncSession

from middleware.db.postgresql import get_session
from models.user import User
from configs.configs import settings
from services.user_service import UserService
from utils.exceptions import UnauthorizedException

bearer = HTTPBearer()


async def login_required(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
        session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise UnauthorizedException()
    except PyJWTError:
        raise UnauthorizedException()

    user = await UserService.get_user_by_username(session=session, username=username)

    if user is None:
        raise UnauthorizedException()

    return user
