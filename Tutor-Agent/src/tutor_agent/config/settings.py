"""Application settings using pydantic-settings."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")

    # Application Settings
    app_name: str = Field(default="TutorGPT", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")

    # Agent Configuration
    default_model: str = Field(default="gpt-4o", description="Default OpenAI model")
    max_turns: int = Field(default=10, description="Maximum conversation turns")
    temperature: float = Field(default=0.7, description="Model temperature")

    # Database (Future)
    database_url: Optional[str] = Field(
        default=None, description="Database connection URL"
    )

    # Redis (Future)
    redis_url: Optional[str] = Field(default=None, description="Redis connection URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Application settings
    """
    return Settings()
