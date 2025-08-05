from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from configs.configs import settings
from models.blog import Blog
from models.blog_tag import BlogTag
from models.project import Project
from models.tag import Tag
from models.user import User


async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
    pool_recycle=settings.SQLALCHEMY_POOL_RECYCLE,
    pool_pre_ping=settings.SQLALCHEMY_POOL_PRE_PING,
    echo=settings.SQLALCHEMY_ECHO
)


async def init_db():
    async with async_engine.begin() as conn:


        await conn.run_sync(SQLModel.metadata.create_all)


def init_sync_engine():
    from sqlmodel import create_engine

    engine = create_engine(
        settings.SQLALCHEMY_SYNC_DATABASE_URI,
        pool_size=settings.SQLALCHEMY_POOL_SIZE,
        max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
        pool_recycle=settings.SQLALCHEMY_POOL_RECYCLE,
        pool_pre_ping=settings.SQLALCHEMY_POOL_PRE_PING,
        echo=settings.SQLALCHEMY_ECHO
    )

    return engine

# AsyncSessionLocal = async_sessionmaker(
#     bind=engine, class_=AsyncSession, autocommit=False, autoflush=False
# )
# Base = declarative_base()


# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session
