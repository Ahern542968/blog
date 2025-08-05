from pydantic import BaseModel


class BlogEntity(BaseModel):
    title: str
    date: str
    tags: list[str]
    draft: bool
    summary: str
    body: dict
    _id: str
    _raw: dict[str, str]
    type: str
    slug: str
    path: str
    filePath: str


class BlogListEntity(BaseModel):
    blogs: list[BlogEntity]
    total: int
