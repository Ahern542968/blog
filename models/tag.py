from typing import List
from uuid import uuid4, UUID

from sqlmodel import Field, Relationship

from models.base import BaseModel


class Tag(BaseModel, table=True):
    __tablename__ = "tags"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
