"""
Application configuration for IntelliICU.

Centralizes environment-specific settings using Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # ----------------------------
    # Project
    # ----------------------------

    PROJECT_NAME: str = "IntelliICU Backend"

    PROJECT_DESCRIPTION: str = (
        "Enterprise AI Clinical Decision Support Platform "
        "for Intensive Care Units."
    )

    PROJECT_VERSION: str = "1.0.0"

    API_V1_PREFIX: str = "/api/v1"

    DEBUG: bool = True

    # ----------------------------
    # Database
    # ----------------------------

    DATABASE_HOST: str = "localhost"

    DATABASE_PORT: int = 5433

    DATABASE_NAME: str = "intelliicu"

    DATABASE_USER: str = "postgres"

    DATABASE_PASSWORD: str = "YOUR_PASSWORD"

    @property
    def DATABASE_URL(self) -> str:
        """
        SQLAlchemy database connection URL.
        """
        return (
            f"postgresql+psycopg://"
            f"{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()