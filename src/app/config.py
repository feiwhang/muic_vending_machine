"""Application configuration."""
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings."""

    db_url: str = Field(..., env="DATABASE_URL")


settings = Settings()
