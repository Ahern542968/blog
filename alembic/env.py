from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

from middleware.db.postgresql import init_sync_engine
from models.blog import Blog
from models.blog_tag import BlogTag
from models.project import Project
from models.tag import Tag
from models.user import User

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

engine = init_sync_engine()
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
