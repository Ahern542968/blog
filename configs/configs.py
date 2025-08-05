from configs.middleware.db.postgresql import DatabaseConfig


class Settings(
    DatabaseConfig,
):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
