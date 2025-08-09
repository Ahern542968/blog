from datetime import date, datetime
from math import ceil
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc, func

from models.user import User
from models.tag import Tag
from schemas.tag import CreateTagVO, DeleteTagVO, AllTagDTO, TagDTO, PageTagDTO
from services.blog_tag_service import BlogTagService
from utils.exceptions import NotFoundException, FlictException


class TagService:

    @staticmethod
    async def get_tag_by_name(session: AsyncSession, current_user: User, tag_name: str) -> Tag:
        result = await session.exec(select(Tag).where(Tag.name == tag_name).where(Tag.created_by == current_user.id))
        return result.first()

    @staticmethod
    async def get_tag_by_id(session: AsyncSession, current_user: User, tag_id: UUID) -> Tag:
        result = await session.exec(select(Tag).where(Tag.id == tag_id).where(Tag.created_by == current_user.id))
        return result.first()

    @staticmethod
    async def create_tags(session: AsyncSession, current_user: User, create_tags_vo: CreateTagVO) -> list[Tag]:
        new_tags = []

        for name in create_tags_vo.tags:
            tag = await TagService.get_tag_by_name(session, current_user, name)
            if tag: continue

            tag = Tag(name=name, created_by=current_user.id)
            session.add(tag)
            new_tags.append(tag)
        await session.commit()

        for tag in new_tags:
            await session.refresh(tag)
        return new_tags

    @staticmethod
    async def delete_tag(session: AsyncSession, current_user: User, delete_tags_vo: DeleteTagVO):
        tag = await TagService.get_tag_by_id(session, current_user, delete_tags_vo.id)
        if not tag: raise NotFoundException()

        blogs = await BlogTagService.get_tag_relationship_blogs(session, tag_ids=[tag.id])
        if blogs: raise FlictException()

        await session.delete(tag)
        await session.commit()

    @staticmethod
    async def get_all_tags(session: AsyncSession, current_user: User) -> list[AllTagDTO]:
        statement = select(Tag).where(Tag.created_by == current_user.id).order_by(desc(Tag.created_at))
        results = await session.exec(statement)
        tags = results.all()

        blogs = await BlogTagService.get_tag_relationship_blogs(session, tag_ids=[tag.id for tag in tags])
        blog_count_map = {}
        for blog_tag in blogs:
            blog_count_map[blog_tag.tag_id] = blog_count_map.get(blog_tag.tag_id, 0) + 1

        tag_dtos = list()
        for tag in tags:
            tag_dto = AllTagDTO.model_validate({**tag.model_dump(), "blog_total": blog_count_map.get(tag.id, 0)})
            tag_dtos.append(tag_dto)
        return tag_dtos

    @staticmethod
    async def get_search_tags(
            session: AsyncSession, current_user: User,
            page_num: int = 1, page_size: int = 10, keyword: str | None = None,
            start_time: date | None = None, end_time: date | None = None
    ) -> PageTagDTO:

        stmt = select(Tag).where(Tag.created_by == current_user.id)
        if keyword:
            stmt = stmt.where(Tag.name.ilike(f"%{keyword}%"))
        if start_time:
            stmt = stmt.where(Tag.created_at >= datetime.combine(start_time, datetime.min.time()))
        if end_time:
            stmt = stmt.where(Tag.created_at <= datetime.combine(end_time, datetime.max.time()))

        total = (await session.exec(
            select(func.count()).select_from(stmt.subquery())
        )).one()

        offset = (page_num - 1) * page_size
        tags = (await session.exec(stmt.order_by(desc(Tag.created_at)).offset(offset).limit(page_size))).all()

        blog_count_map = {}
        if tags:
            blogs = await BlogTagService.get_tag_relationship_blogs(session, tag_ids=[t.id for t in tags])
            for blog in blogs:
                blog_count_map[blog.tag_id] = blog_count_map.get(blog.tag_id, 0) + 1

        tag_dtos = [
            TagDTO.model_validate({
                **t.model_dump(),
                "blog_total": blog_count_map.get(t.id, 0)}
            )
            for t in tags
        ]

        return PageTagDTO(
            tags=tag_dtos,
            total=total,
            page_size=page_size,
            page_num=page_num,
            pages=ceil(total / page_size) if page_size else 0
        )