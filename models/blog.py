from typing import Optional, List
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from models.base import BaseModel


class Blog(BaseModel, table=True):
    __tablename__ = "blogs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    summary: str
    markdown_content: str
    compiled_content: str
    author_id: UUID = Field(index=True)
    project_id: Optional[UUID] = Field(default=None, index=True)

