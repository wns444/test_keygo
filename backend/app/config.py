import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", "sqlite:///./test_keygo.db"
    )

    # App
    app_name: str = "KeyGo Internal Task Tracker"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"


settings = Settings()
