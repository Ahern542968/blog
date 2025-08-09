from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import status, Depends, Body, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from depends.user import login_required
from middleware.db.postgresql import get_session
from models.user import User
from schemas.tag import CreateTagVO, DeleteTagVO, PageTagVO, TagDTO
from services.tag_service import TagService
from utils.exception_handlers import APIResponse

router = APIRouter(prefix="/admin/tags", tags=["标签管理"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_tag(
        create_tags_vo: Annotated[CreateTagVO, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
        current_user: Annotated[User, Depends(login_required)],
):
    tags = await TagService.create_tags(session, current_user, create_tags_vo)
    return APIResponse.success([TagDTO.model_validate(tag) for tag in tags])


@router.delete("", status_code=status.HTTP_200_OK)
async def delete_tag(
        delete_tags_vo: Annotated[DeleteTagVO, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
        current_user: Annotated[User, Depends(login_required)],
):
    await TagService.delete_tag(session, current_user, delete_tags_vo)
    return APIResponse.success()


@router.get("", status_code=status.HTTP_200_OK)
async def all_tags(
        session: Annotated[AsyncSession, Depends(get_session)],
        current_user: Annotated[User, Depends(login_required)],
):
    tags = await TagService.get_all_tags(session, current_user=current_user)
    return APIResponse.success(tags)


@router.get("/list", status_code=status.HTTP_200_OK)
async def list_tags(
        vo: Annotated[PageTagVO, Query()],
        session: Annotated[AsyncSession, Depends(get_session)],
        current_user: Annotated[User, Depends(login_required)],
):
    tags = await TagService.get_search_tags(
        session=session, current_user=current_user,
        page_num=vo.page_num, page_size=vo.page_size,
        keyword=vo.name, start_time=vo.start_date, end_time=vo.end_date
    )
    return APIResponse.success(tags)
