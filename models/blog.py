from typing import Optional
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

    author: Optional["User"] = Relationship(
        back_populates="blogs",
        sa_relationship_kwargs={
            "primaryjoin": "foreign(Blog.author_id) == User.id",
            "viewonly": True,
        }
    )
    project: Optional["Project"] = Relationship(
        back_populates="blogs",
        sa_relationship_kwargs={
            "primaryjoin": "foreign(Blog.project_id) == Project.id",
            "viewonly": True,
        }
    )
    blog_tags: list["BlogTag"] = Relationship(
        back_populates="blog"
    )

    @property
    def tags(self) -> list["Tag"]:
        return [bt.tag for bt in self.blog_tags]
