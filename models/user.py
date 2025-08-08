from typing import Optional, List
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from models.base import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True)
    hash_password: str

    email: Optional[str] = Field(default=None, description="邮箱")
    position: Optional[str] = Field(default=None, description="职位")
    bio: Optional[str] = Field(default=None, description="个人简介")