"""
Application configuration via Pydantic BaseSettings.

All settings are read from environment variables (or .env file).
"""

from __future__ import annotations

from typing import Optional

from pydantic import computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Signing keys that appear in this repository. Anyone can forge tokens with them.
_PUBLISHED_SECRET_KEYS = {
    "change-me-to-a-long-random-string-at-least-32-chars",
    "your-super-secret-key-change-this-in-production-at-least-32-chars",
    "test-secret-key-for-ci-only",
}
_LOCAL_ENVIRONMENTS = {"development", "test"}
_MIN_SECRET_KEY_LENGTH = 32


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        # Validation errors would otherwise echo secrets into startup logs.
        hide_input_in_errors=True,
    )

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://jobsense:jobsense@localhost:5432/jobsense"

    @computed_field  # type: ignore[misc]
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Derive asyncpg URL from sync DATABASE_URL."""
        url = self.DATABASE_URL
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Auth / Security ───────────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-to-a-long-random-string-at-least-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # ── AI Providers ──────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DEFAULT_LLM_PROVIDER: str = "openai"  # openai | anthropic

    # ── Apify ─────────────────────────────────────────────────────────────────
    APIFY_API_TOKEN: str = ""

    # ── Google OAuth ──────────────────────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    # ── AWS / S3 ──────────────────────────────────────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "jobsense-documents"

    # ── Observability ─────────────────────────────────────────────────────────
    SENTRY_DSN: Optional[str] = None
    POSTHOG_KEY: Optional[str] = None

    # ── App ───────────────────────────────────────────────────────────────────
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    FRONTEND_URL: str = "http://localhost:3000"

    @computed_field  # type: ignore[misc]
    @property
    def CORS_ORIGINS(self) -> list[str]:
        """Build CORS origins list."""
        origins = [self.FRONTEND_URL]
        if self.ENVIRONMENT == "development":
            origins += [
                "http://localhost:3000",
                "http://localhost:3001",
                "http://127.0.0.1:3000",
            ]
        return list(set(origins))

    @model_validator(mode="after")
    def require_private_secret_key(self) -> "Settings":
        """Refuse to start a deployed environment with a guessable signing key."""
        if self.ENVIRONMENT in _LOCAL_ENVIRONMENTS:
            return self
        if (
            self.SECRET_KEY in _PUBLISHED_SECRET_KEYS
            or len(self.SECRET_KEY) < _MIN_SECRET_KEY_LENGTH
        ):
            raise ValueError(
                "SECRET_KEY must be a private random value of at least 32 characters "
                "when ENVIRONMENT is not development or test"
            )
        return self


# Singleton instance — import this throughout the codebase
settings = Settings()
