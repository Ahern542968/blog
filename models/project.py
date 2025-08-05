from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from models.base import BaseModel


class Project(BaseModel, table=True):
    __tablename__ = "projects"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str] = None

    blogs: list["Blog"] = Relationship(back_populates="project")
