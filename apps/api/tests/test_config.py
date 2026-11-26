"""
Settings validation. These tests need no database.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.config import Settings

PRIVATE_KEY = "unit-test-signing-key-0123456789abcdef"


@pytest.mark.parametrize("environment", ["production", "staging"])
@pytest.mark.parametrize(
    "secret_key",
    [
        "change-me-to-a-long-random-string-at-least-32-chars",
        "your-super-secret-key-change-this-in-production-at-least-32-chars",
        "too-short",
        "",
    ],
)
def test_deployed_environment_rejects_weak_secret_key(environment: str, secret_key: str):
    with pytest.raises(ValidationError) as error:
        Settings(_env_file=None, ENVIRONMENT=environment, SECRET_KEY=secret_key)

    assert "SECRET_KEY" in str(error.value)
    assert "input_value" not in str(error.value)


def test_deployed_environment_accepts_private_secret_key():
    settings = Settings(_env_file=None, ENVIRONMENT="production", SECRET_KEY=PRIVATE_KEY)

    assert settings.SECRET_KEY == PRIVATE_KEY


def test_local_development_still_starts_with_the_default_key():
    assert Settings(_env_file=None, ENVIRONMENT="development").SECRET_KEY
