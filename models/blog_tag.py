from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from models.base import BaseModel

class BlogTag(BaseModel, table=True):
    __tablename__ = "blog_tags"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    blog_id: UUID = Field(index=True)
    tag_id: UUID = Field(index=True)
