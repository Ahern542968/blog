from configs.middleware.db.postgresql import DatabaseConfig
from configs.middleware.project import ProjectConfig


class Settings(
    DatabaseConfig,
    ProjectConfig,
):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
