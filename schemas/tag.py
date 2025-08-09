from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, field_serializer


class CreateTagVO(BaseModel):
    tags: list[str]


class DeleteTagVO(BaseModel):
    id: UUID


class PageTagVO(BaseModel):
    name: str | None = None
    page_num: int = 1
    page_size: int = 10
    start_date: date | None = None
    end_date: date | None = None


class AllTagDTO(BaseModel):
    id: UUID
    name: str
    blog_total: int | None = None

    class Config:
        from_attributes = True


class TagDTO(AllTagDTO):
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_serializer('created_at')
    def serialize_created_at(self, v: datetime):
        if v is None:
            return None
        return v.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer('updated_at')
    def serialize_updated_at(self, v: datetime):
        if v is None:
            return None
        return v.strftime("%Y-%m-%d %H:%M:%S")


class PageTagDTO(BaseModel):
    tags: list[TagDTO]
    total: int
    page_size: int
    page_num: int
    pages: int
