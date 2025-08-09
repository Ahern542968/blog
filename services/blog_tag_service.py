from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from models.blog_tag import BlogTag


class BlogTagService:

    @staticmethod
    async def get_tag_relationship_blogs(session: AsyncSession, tag_ids: list[UUID]) -> list[BlogTag]:
        result = await session.exec(select(BlogTag).where(BlogTag.tag_id.in_(tag_ids)))
        return result.all()

    @staticmethod
    async def get_blog_relationship_tags(session: AsyncSession, blog_ids: list[UUID]) -> list[BlogTag]:
        result = await session.exec(select(BlogTag).where(BlogTag.blog_id.in_(blog_ids)))
        return result.all()
