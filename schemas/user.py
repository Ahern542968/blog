import uuid

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    id: uuid.UUID
    username: str
    email: str | None
    position: str | None
    bio: str | None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UpdatePasswordInput(BaseModel):
    old_password: str
    new_password: str
