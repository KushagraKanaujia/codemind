"""
Application configuration using Pydantic settings.
Loads from environment variables with validation.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # AI APIs
    anthropic_api_key: str = Field(..., alias="ANTHROPIC_API_KEY")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")

    # Supabase
    supabase_url: str = Field(..., alias="SUPABASE_URL")
    supabase_key: str = Field(..., alias="SUPABASE_KEY")
    supabase_service_key: Optional[str] = Field(None, alias="SUPABASE_SERVICE_KEY")

    # Redis
    redis_url: str = Field("redis://localhost:6379", alias="REDIS_URL")
    redis_password: Optional[str] = Field(None, alias="REDIS_PASSWORD")

    # Application
    env: str = Field("development", alias="ENV")
    debug: bool = Field(True, alias="DEBUG")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    # API
    api_v1_prefix: str = Field("/api/v1", alias="API_V1_PREFIX")
    max_search_results: int = Field(10, alias="MAX_SEARCH_RESULTS")
    cache_ttl: int = Field(3600, alias="CACHE_TTL")

    # Rate Limiting
    rate_limit_per_minute: int = Field(60, alias="RATE_LIMIT_PER_MINUTE")

    # CORS
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
