from uuid import uuid4, UUID

from sqlmodel import Field

from models.base import BaseModel


class Tag(BaseModel, table=True):
    __tablename__ = "tags"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    created_by: UUID = Field(nullable=False)
