from pydantic import Field
from pydantic_settings import BaseSettings


class ProjectConfig(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token 有效时间（分钟）"
    )

    SECRET_KEY: str = Field(
        default="secret-key",
        description="JWT加密密钥"
    )

    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="JWT加密算法"
    )

    ACCESS_TOKEN_TYPE: str = Field(
        default="Bearer",
        description="访问令牌类型"
    )

    ROUTER_PREFIX: str = Field(
        default="/api/v1",
        description="路由前缀"
    )
