from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from models.base import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True)
    email: str
    position: Optional[str] = Field(default=None, description="职位")
    bio: Optional[str] = Field(default=None, description="个人简介")

    blogs: list["Blog"] = Relationship(back_populates="author")
