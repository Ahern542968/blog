from datetime import datetime

from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column


class BaseModel(SQLModel, table=False):

    id: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4),
    )
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.model_dump()}>"
