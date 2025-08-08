from typing import Annotated

from fastapi import Depends, Body
from fastapi.routing import APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from depends.user import login_required
from schemas.user import BaseUser, UserInfo, Token, UpdatePasswordInput
from services.user_service import UserService
from fastapi import status

from middleware.db.postgresql import get_session
from models.user import User
from utils.exception_handlers import APIResponse

router = APIRouter(prefix="/users", tags=["用户"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
        user: Annotated[BaseUser, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
):
    new_user = await UserService.create_user(session, user.username, user.password)
    return APIResponse.success(UserInfo.model_validate(new_user))


@router.get("", status_code=status.HTTP_200_OK)
async def list_users(
        session: Annotated[AsyncSession, Depends(get_session)],
        skip: int = 0,
        limit: int = 100,
):
    users = await UserService.get_users(session, skip=skip, limit=limit)
    return APIResponse.success([UserInfo.model_validate(user) for user in users])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
        user: Annotated[BaseUser, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
):
    token = await UserService.login(session, user.username, user.password)
    return APIResponse.success(token)


@router.get("/me", status_code=status.HTTP_200_OK)
async def me(current_user: Annotated[User, Depends(login_required)]):
    return APIResponse.success(UserInfo.model_validate(current_user))


@router.post("/password/update", status_code=status.HTTP_200_OK)
async def update_password(
        data: Annotated[UpdatePasswordInput, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
        current_user: Annotated[User, Depends(login_required)],
):
    user = await UserService.update_password(session, current_user.username, data.old_password, data.new_password)
    return APIResponse.success(UserInfo.model_validate(user))
