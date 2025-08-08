from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from configs.configs import settings

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
    pool_recycle=settings.SQLALCHEMY_POOL_RECYCLE,
    pool_pre_ping=settings.SQLALCHEMY_POOL_PRE_PING,
    echo=settings.SQLALCHEMY_ECHO,
)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_db():
    async with async_engine.begin() as conn:
        from models.blog import Blog
        from models.blog_tag import BlogTag
        from models.project import Project
        from models.tag import Tag
        from models.user import User
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


def init_sync_engine():
    engine = create_engine(
        settings.SQLALCHEMY_SYNC_DATABASE_URI,
        pool_size=settings.SQLALCHEMY_POOL_SIZE,
        max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
        pool_recycle=settings.SQLALCHEMY_POOL_RECYCLE,
        pool_pre_ping=settings.SQLALCHEMY_POOL_PRE_PING,
        echo=settings.SQLALCHEMY_ECHO,
    )
    return engine
