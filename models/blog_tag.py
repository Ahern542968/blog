from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from models.base import BaseModel

class BlogTag(BaseModel, table=True):
    __tablename__ = "blog_tags"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    blog_id: UUID = Field(index=True)
    tag_id: UUID = Field(index=True)

    blog: "Blog" = Relationship(
        back_populates="blog_tags",
        sa_relationship_kwargs={
            "primaryjoin": "foreign(BlogTag.blog_id) == Blog.id",
            "viewonly": True,
        }
    )
    tag: "Tag" = Relationship(
        back_populates="blog_tags",
        sa_relationship_kwargs={
            "primaryjoin": "foreign(BlogTag.tag_id) == Tag.id",
            "viewonly": True,
        }
    )