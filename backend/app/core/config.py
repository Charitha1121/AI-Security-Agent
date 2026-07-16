"""
Application configuration using Pydantic Settings.

This module centralizes all environment-driven configuration for the
AI Security Agent backend.
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================================================
    # API Configuration
    # ==========================================================
    APP_NAME: str = Field(default="AI Security Agent")
    APP_VERSION: str = Field(default="0.1.0")
    API_V1_PREFIX: str = Field(default="/api/v1")
    DEBUG: bool = Field(default=False)

    # ==========================================================
    # Server Configuration
    # ==========================================================
    ENVIRONMENT: str = Field(default="development")
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # ==========================================================
    # JWT Authentication
    # ==========================================================
    SECRET_KEY: str = Field(default="change-this-later")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    # ==========================================================
    # CORS Configuration
    # ==========================================================
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173"
    )

    # ==========================================================
    # Database Configuration
    # ==========================================================
    DATABASE_URL: str = Field(
    default="sqlite:///./ai_security_agent.db"
)

    DATABASE_ECHO: bool = Field(default=False)

    # ==========================================================
    # Logging Configuration
    # ==========================================================
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="text")

    # ==========================================================
    # Upload Configuration
    # ==========================================================
    UPLOAD_DIR: str = Field(default="app/uploads")
    REPORT_DIR: str = Field(default="app/reports")
    MAX_UPLOAD_SIZE: int = Field(default=100 * 1024 * 1024)  # 100 MB

    # ==========================================================
    # Validators
    # ==========================================================
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        """Normalize environment name."""
        return value.lower()

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Normalize log level."""
        return value.upper()

    # ==========================================================
    # Helper Properties
    # ==========================================================
    @property
    def cors_origins(self) -> list[str]:
        """Return CORS origins as a list."""
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()